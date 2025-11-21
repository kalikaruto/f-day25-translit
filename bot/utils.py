# utils.py

from enum import Enum
from pydantic import BaseModel

class Lang(str, Enum):
    as_ = "as"      # Assamese - অসমীয়া
    bn  = "bn"      # Bangla - বাংলা
    brx = "brx"     # Boro - बड़ो
    gu  = "gu"      # Gujarati - ગુજરાતી
    hi  = "hi"      # Hindi - हिंदी
    kn  = "kn"      # Kannada - ಕನ್ನಡ
    ks  = "ks"      # Kashmiri - كٲشُر
    gom = "gom"     # Konkani Goan - कोंकणी
    mai = "mai"     # Maithili - मैथिली
    ml  = "ml"      # Malayalam - മലയാളം
    mni = "mni"     # Manipuri - ꯃꯤꯇꯩꯂꯣꯟ
    mr  = "mr"      # Marathi - मराठी
    ne  = "ne"      # Nepali - नेपाली
    or_ = "or"      # Oriya - ଓଡ଼ିଆ
    pa  = "pa"      # Panjabi - ਪੰਜਾਬੀ
    sa  = "sa"      # Sanskrit - संस्कृतम्
    sd  = "sd"      # Sindhi - سنڌي
    si  = "si"      # Sinhala - සිංහල
    ta  = "ta"      # Tamil - தமிழ்
    te  = "te"      # Telugu - తెలుగు
    ur  = "ur"      # Urdu - اُردُو

class SrcLang(str, Enum):
    roman  = "roman"      # Roman - English
    indic = "indic" # Indic - Indic

class Input(BaseModel):
    text: str
    lang: Lang
    srclang: SrcLang

class LangReq(BaseModel):
    lang: Lang

LANG_INFO = [
    {"code": "as",  "label": "Assamese - অসমীয়া"},
    {"code": "bn",  "label": "Bangla - বাংলা"},
    {"code": "brx", "label": "Boro - बड़ो"},
    {"code": "gu",  "label": "Gujarati - ગુજરાતી"},
    {"code": "hi",  "label": "Hindi - हिंदी"},
    {"code": "kn",  "label": "Kannada - ಕನ್ನಡ"},
    {"code": "ks",  "label": "Kashmiri - كٲشُر"},
    {"code": "gom", "label": "Konkani Goan - कोंकणी"},
    {"code": "mai", "label": "Maithili - मैथिली"},
    {"code": "ml",  "label": "Malayalam - മലയാളം"},
    {"code": "mni", "label": "Manipuri - ꯃꯤꯇꯩꯂꯣꯟ"},
    {"code": "mr",  "label": "Marathi - मराठी"},
    {"code": "ne",  "label": "Nepali - नेपाली"},
    {"code": "or",  "label": "Oriya - ଓଡ଼ିଆ"},
    {"code": "pa",  "label": "Panjabi - ਪੰਜਾਬੀ"},
    {"code": "sa",  "label": "Sanskrit - संस्कृतम्"},
    {"code": "sd",  "label": "Sindhi - سنڌي"},
    {"code": "si",  "label": "Sinhala - සිංහල"},
    {"code": "ta",  "label": "Tamil - தமிழ்"},
    {"code": "te",  "label": "Telugu - తెలుగు"},
    {"code": "ur",  "label": "Urdu - اُردُو"},
]

SRC_SCRIPT_TYPES_INFO = [
    {"code": "roman", "label": "Roman - English"},
    {"code": "indic", "label": "Indic - Indic"},
]