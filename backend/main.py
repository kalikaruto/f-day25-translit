from fastapi import FastAPI
from utils import *
import torch, argparse
from ai4bharat.transliteration import XlitEngine

torch.serialization.add_safe_globals([argparse.Namespace])

app = FastAPI()

engines = {}

def get_engine(lang, src):
    key = (src.value, lang.value)
    if key not in engines:
        engines[key] = XlitEngine(
            lang.value,
            beam_width=10,
            rescore=True,
            src_script_type=src.value
        )
    return engines[key]

@app.post("/transliterate/sentence")
async def transliterate_sentence(data: Input):
    engine = get_engine(data.lang, data.srclang)
    out = engine.translit_sentence(data.text, lang_code=data.lang.value)
    return {
        "input": data.text,
        "srclang": data.srclang.value,
        "lang": data.lang.value,
        "output": out
    }

@app.get("/lang/list")
async def list_langs():
    return {"lang_codes": LANG_INFO, "src_script_types": SRC_SCRIPT_TYPES_INFO}
