from fastapi import FastAPI
from pydantic import BaseModel
import torch, argparse
from ai4bharat.transliteration import XlitEngine

torch.serialization.add_safe_globals([argparse.Namespace])
e = XlitEngine("hi", beam_width=10, rescore=True)

app = FastAPI()

class Input(BaseModel):
    text: str

@app.post("/transliterate/word")
def transliterate(data: Input):
    out = e.translit_word(data.text, topk=5)
    return {"input": data.text, "output": out}

@app.post("/transliterate/sentence")
def transliterate_sentence(data: Input):
    out = e.translit_sentence(data.text)
    return {"input": data.text, "output": out}

