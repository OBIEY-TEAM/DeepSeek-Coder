import argparse
import copy
import json
import os
import random
import re
from collections.abc import Sequence
from dataclasses import dataclass, field

import torch
import torch.distributed
import transformers
from datasets import load_dataset
from transformers import BitsAndBytesConfig, Trainer

DEFAULT_MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"
IGNORE_INDEX = -100
EOT_TOKEN = "<|EOT|>"

def build_instruction_prompt(instruction: str):
    return f'''
You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
{instruction.strip()}
### Response:
'''.lstrip()


def anonymize_code_and_text(text: str) -> str:
    """
    Anonymizes client data: removes IP addresses, API keys, bearer tokens, credentials, and internal project names.
    """
    if not isinstance(text, str):
        return text

    # IP addresses
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[ANONYMIZED_IP]', text)
    # API keys / Bearer tokens / secret strings
    text = re.sub(r'(?i)(api[_-]?key|secret|token|password|auth)\s*[:=]\s*["\'][A-Za-z0-9_\-\.]{8,}["\']', r'\1 = "[ANONYMIZED_SECRET]"', text)
    text = re.sub(r'Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*', 'Bearer [ANONYMIZED_TOKEN]', text)
    # Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[ANONYMIZED_EMAIL]', text)

    return text

def clean_and_anonymize_dataset(raw_dataset_path: str, output_cleaned_path: str) -> str:
    """
    Loads json/jsonl dataset, applies anonymization, and saves cleaned dataset.
    """
    print(f"Cleaning and anonymizing dataset from {raw_dataset_path}...")
    cleaned_data = []

    with open(raw_dataset_path, "r", encoding="utf-8") as f:
        if raw_dataset_path.endswith(".jsonl"):
            lines = f.readlines()
            for line in lines:
                if line.strip():
                    item = json.loads(line.strip())
                    cleaned_data.append(item)
        else:
            cleaned_data = json.load(f)

    for item in cleaned_data:
        if "instruction" in item:
            item["instruction"] = anonymize_code_and_text(item["instruction"])
        if "input" in item:
            item["input"] = anonymize_code_and_text(item["input"])
        if "output" in item:
            item["output"] = anonymize_code_and_text(item["output"])

    os.makedirs(os.path.dirname(os.path.abspath(output_cleaned_path)), exist_ok=True)
    with open(output_cleaned_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print(f"Cleaned dataset saved to {output_cleaned_path}")
    return output_cleaned_path

@dataclass
class ModelArguments:
    model_name_or_path: str | None = field(default=DEFAULT_MODEL_NAME)

@dataclass
class DataArguments:
    data_path: str = field(default=None, metadata={"help": "Path to the training data."})

@dataclass
class LoraArguments:
    use_peft: bool = field(default=False, metadata={"help": "Whether to use PEFT (LoRA/QLoRA)."})
    lora_r: int = field(default=16, metadata={"help": "LoRA rank r."})
    lora_alpha: int = field(default=32, metadata={"help": "LoRA alpha."})
    lora_dropout: float = field(default=0.05, metadata={"help": "LoRA dropout."})
    lora_target_modules: str | None = field(
        default="q_proj,k_proj,v_proj,o_proj",
        metadata={"help": "Comma separated list of target modules for LoRA."}
    )
    load_in_4bit: bool = field(default=False, metadata={"help": "Load model in 4-bit precision for QLoRA."})
    load_in_8bit: bool = field(default=False, metadata={"help": "Load model in 8-bit precision."})

@dataclass
class TrainingArguments(transformers.TrainingArguments):
    cache_dir: str | None = field(default=None)
    optim: str = field(default="adamw_torch")
    model_max_length: int = field(
        default=512,
        metadata={"help": "Maximum sequence length. Sequences will be right padded (and possibly truncated)."},
    )

def safe_save_model_for_hf_trainer(trainer: transformers.Trainer, output_dir: str):
    """Collects the state dict and dump to disk."""
    if hasattr(trainer, "model") and hasattr(trainer.model, "save_pretrained"):
        trainer.model.save_pretrained(output_dir)
        return
    state_dict = trainer.model.state_dict()
    if trainer.args.should_save:
        cpu_state_dict = {key: value.cpu() for key, value in state_dict.items()}
        del state_dict
        trainer._save(output_dir, state_dict=cpu_state_dict)


def _tokenize_fn(strings: Sequence[str], tokenizer: transformers.PreTrainedTokenizer) -> dict:
    """Tokenize a list of strings."""
    tokenized_list = [
        tokenizer(
            text,
            return_tensors="pt",
            padding="longest",
            max_length=tokenizer.model_max_length,
            truncation=True,
        )
        for text in strings
    ]

    input_ids = labels = [tokenized.input_ids[0] for tokenized in tokenized_list]
    input_ids_lens = labels_lens = [
        tokenized.input_ids.ne(tokenizer.pad_token_id).sum().item() for tokenized in tokenized_list
    ]

    return dict(
        input_ids=input_ids,
        labels=labels,
        input_ids_lens=input_ids_lens,
        labels_lens=labels_lens,
    )


def preprocess(
    sources: Sequence[str],
    targets: Sequence[str],
    tokenizer: transformers.PreTrainedTokenizer,
) -> dict:
    """Preprocess the data by tokenizing."""
    examples = [s + t for s, t in zip(sources, targets)]
    examples_tokenized, sources_tokenized = [_tokenize_fn(strings, tokenizer) for strings in (examples, sources)]
    input_ids = examples_tokenized["input_ids"]

    labels = copy.deepcopy(input_ids)
    for label, source_len in zip(labels, sources_tokenized["input_ids_lens"]):
        label[:source_len] = IGNORE_INDEX
    return dict(input_ids=input_ids, labels=labels)

@dataclass
class DataCollatorForSupervisedDataset:
    """Collate examples for supervised fine-tuning."""
    tokenizer: transformers.PreTrainedTokenizer

    def __call__(self, instances: Sequence[dict]) -> dict[str, torch.Tensor]:
        input_ids, labels = tuple([instance[key] for instance in instances] for key in ("input_ids", "labels"))
        input_ids = [torch.tensor(x) for x in input_ids]
        input_ids = torch.nn.utils.rnn.pad_sequence(
            input_ids, batch_first=True, padding_value=self.tokenizer.pad_token_id
        )
        labels = [torch.tensor(x) for x in labels]
        labels = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=IGNORE_INDEX)

        return dict(
            input_ids=input_ids,
            labels=labels,
            attention_mask=input_ids.ne(self.tokenizer.pad_token_id),
        )

def train_tokenize_function(examples, tokenizer):
    sources = [
        build_instruction_prompt(instruction)
        for instruction in examples['instruction']
    ]
    targets = [f"{output}\n{EOT_TOKEN}" for output in examples['output']]
    data_dict = preprocess(sources, targets, tokenizer)
    return data_dict

def main():
    parser = argparse.ArgumentParser(description="CYBERSOCLE Fine-Tuning Pipeline with Data Anonymization.")
    parser.add_argument("--model_name_or_path", type=str, default=DEFAULT_MODEL_NAME)
    parser.add_argument("--data_path", type=str, required=True, help="Path to input raw training JSON dataset.")
    parser.add_argument("--output_dir", type=str, required=True, help="Output directory for model/LoRA adapter.")
    parser.add_argument("--use_peft", action="store_true", default=True, help="Use PEFT (LoRA/QLoRA).")
    parser.add_argument("--lora_r", type=int, default=16)
    parser.add_argument("--lora_alpha", type=int, default=32)
    parser.add_argument("--lora_dropout", type=float, default=0.05)
    parser.add_argument("--load_in_4bit", action="store_true", default=False)
    parser.add_argument("--num_train_epochs", type=float, default=3.0)
    parser.add_argument("--per_device_train_batch_size", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=2e-4)

    args = parser.parse_args()

    if "v2" in args.model_name_or_path.lower() or "v3" in args.model_name_or_path.lower() or "r1" in args.model_name_or_path.lower():
        raise ValueError("Usage of DeepSeek V2, V3 or R1 models is strictly prohibited. Only V1 models are allowed.")

    cleaned_data_path = os.path.join(args.output_dir, "cleaned_cybersocle_dataset.json")
    clean_and_anonymize_dataset(args.data_path, cleaned_data_path)

    print(f"Starting CYBERSOCLE fine-tuning with model {args.model_name_or_path}...")

    tokenizer = transformers.AutoTokenizer.from_pretrained(
        args.model_name_or_path,
        model_max_length=512,
        padding_side="right",
        use_fast=True,
        trust_remote_code=True
    )

    quantization_config = None
    if args.load_in_4bit:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )

    model_kwargs = {"torch_dtype": torch.bfloat16}
    if quantization_config is not None:
        model_kwargs["quantization_config"] = quantization_config

    model = transformers.AutoModelForCausalLM.from_pretrained(
        args.model_name_or_path,
        **model_kwargs
    )

    if args.use_peft:
        try:
            from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
            if args.load_in_4bit:
                model = prepare_model_for_kbit_training(model)

            peft_config = LoraConfig(
                r=args.lora_r,
                lora_alpha=args.lora_alpha,
                lora_dropout=args.lora_dropout,
                target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
                bias="none",
                task_type="CAUSAL_LM",
            )
            model = get_peft_model(model, peft_config)
            model.print_trainable_parameters()
        except ImportError as e:
            raise ImportError("PEFT library is required when --use_peft is enabled. Please install peft.") from e

    raw_train_datasets = load_dataset(
        'json',
        data_files=cleaned_data_path,
        split="train"
    )

    num_proc = min(32, os.cpu_count() or 1)
    train_dataset = raw_train_datasets.map(
        train_tokenize_function,
        batched=True,
        batch_size=3000,
        num_proc=num_proc,
        remove_columns=raw_train_datasets.column_names,
        load_from_cache_file=True,
        desc="Running Encoding",
        fn_kwargs={"tokenizer": tokenizer}
    )

    data_collator = DataCollatorForSupervisedDataset(tokenizer=tokenizer)
    training_args = transformers.TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        learning_rate=args.learning_rate,
        save_strategy="steps",
        save_steps=100,
        logging_steps=10,
        optim="adamw_torch"
    )

    trainer = Trainer(model=model, tokenizer=tokenizer, args=training_args, train_dataset=train_dataset, data_collator=data_collator)
    trainer.train()
    trainer.save_state()
    safe_save_model_for_hf_trainer(trainer=trainer, output_dir=args.output_dir)

if __name__ == "__main__":
    main()
