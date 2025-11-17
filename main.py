# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import torch, argparse
from ai4bharat.transliteration import XlitEngine

from utils import *

torch.serialization.add_safe_globals([argparse.Namespace])

app = FastAPI()

# Cache engines here
engines = {}

def get_engine(lang: str):
    if lang not in engines:
        engines[lang] = XlitEngine(lang, beam_width=10, rescore=True)
    return engines[lang]


@app.post("/transliterate/word")
def transliterate_word(data: Input):
    engine = get_engine(data.outlang.value)
    out = engine.translit_word(data.text, topk=5)
    return {"input": data.text, "outlang": data.outlang.value, "output": out}


@app.post("/transliterate/sentence")
def transliterate_sentence(data: Input):
    engine = get_engine(data.outlang.value)
    out = engine.translit_sentence(data.text)
    return {"input": data.text, "outlang": data.outlang.value, "output": out}


@app.get("/outlang")
def get_outlangs():
    return {"note": "Use the 'name' fields for querying instead of 'code' fields.", "supported": LANG_INFO}


@app.post("/outlang")
def set_lang(data: LangReq):
    try:
        get_engine(data.outlang.value)
        return {"ok": True, "outlang": data.outlang.value}
    except Exception:
        return {"ok": False, "error": "Unsupported language"}

