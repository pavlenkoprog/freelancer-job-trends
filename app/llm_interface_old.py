import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# MODEL_NAME = "defog/sqlcoder-7b-2"
MODEL_NAME = "PipableAI/pip-library-etl-1.3b"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(BASE_DIR, "../data/prompt.md")
METADATA_FILE = os.path.join(BASE_DIR, "../data/metadata.sql")

def generate_prompt(question):
    print(os.getcwd())
    with open(PROMPT_FILE, "r") as f:
        prompt = f.read()
    with open(METADATA_FILE, "r") as f:
        metadata = f.read()
    return prompt.format(user_question=question, table_metadata_string=metadata)

def get_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto",
        # torch_dtype=torch.float32,
        # device_map="cpu",
    )
    return tokenizer, model

def generate_sql(question: str) -> str:
    tokenizer, model = get_model()
    prompt = generate_prompt(question)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=300,
        return_full_text=False,
        # do_sample=False,
        # num_beams=5,
        do_sample=True,
        num_beams=1,
        temperature=0.7,
    )
    eos_token_id = tokenizer.eos_token_id

    response = pipe(
        prompt,
        num_return_sequences=1,
        eos_token_id=eos_token_id,
        pad_token_id=eos_token_id,
    )[0]["generated_text"]

    print(response)

    sql_query = (
        response.split(";")[0]
        .split("```")[0]
        .strip()
        + ";"
    )

    return sql_query
