from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
torch.manual_seed(42)

# model_name = "t-tech/T-pro-it-1.0"
model_name = "t-tech/T-lite-it-1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
)

prompt = "Напиши стих про цифровую кафедру сеченовского университета"
messages = [
    {"role": "system", "content": "Ты профессиональный виртуальный ассистент. Твоя спецмализация - медицинские знания. Тебя обучали в Институте цифровой медицины Сеченовского университета. Твоя задача - быть полезным диалоговым ассистентом."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=256
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(response)
