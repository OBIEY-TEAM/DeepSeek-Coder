## How to Fine-tune CYBERSOCLE

We provide script `finetune_cybersocle.py` for users to finetune models on downstream cybersecurity tasks with automatic data anonymization.

Install required packages by:

```bash
pip install -r requirements.txt
```

Please follow the sample dataset format to prepare your training data. Each line is a json-serialized string or json list with required fields `instruction`, `input` (optional), and `output`.

After data preparation, you can use `finetune_cybersocle.py` to train your LoRA adapter:

```bash
DATA_PATH="<your_data_path>"
OUTPUT_PATH="<your_output_path>"
MODEL_PATH="deepseek-ai/deepseek-coder-6.7b-instruct"

python finetune/finetune_cybersocle.py \
    --model_name_or_path $MODEL_PATH \
    --data_path $DATA_PATH \
    --output_dir $OUTPUT_PATH \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --learning_rate 2e-4 \
    --use_peft \
    --load_in_4bit
```
