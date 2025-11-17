# utils.py

from enum import Enum
from pydantic import BaseModel

class OutLang(str, Enum):
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

class Input(BaseModel):
    text: str
    outlang: OutLang

class LangReq(BaseModel):
    outlang: OutLang

LANG_INFO = [
    {"name": "as_", "code": "as",  "label": "Assamese - অসমীয়া"},
    {"name": "bn",  "code": "bn",  "label": "Bangla - বাংলা"},
    {"name": "brx", "code": "brx", "label": "Boro - बड़ो"},
    {"name": "gu",  "code": "gu",  "label": "Gujarati - ગુજરાતી"},
    {"name": "hi",  "code": "hi",  "label": "Hindi - हिंदी"},
    {"name": "kn",  "code": "kn",  "label": "Kannada - ಕನ್ನಡ"},
    {"name": "ks",  "code": "ks",  "label": "Kashmiri - كٲشُر"},
    {"name": "gom", "code": "gom", "label": "Konkani Goan - कोंकणी"},
    {"name": "mai", "code": "mai", "label": "Maithili - मैथिली"},
    {"name": "ml",  "code": "ml",  "label": "Malayalam - മലയാളം"},
    {"name": "mni", "code": "mni", "label": "Manipuri - ꯃꯤꯇꯩꯂꯣꯟ"},
    {"name": "mr",  "code": "mr",  "label": "Marathi - मराठी"},
    {"name": "ne",  "code": "ne",  "label": "Nepali - नेपाली"},
    {"name": "or_", "code": "or",  "label": "Oriya - ଓଡ଼ିଆ"},
    {"name": "pa",  "code": "pa",  "label": "Panjabi - ਪੰਜਾਬੀ"},
    {"name": "sa",  "code": "sa",  "label": "Sanskrit - संस्कृतम्"},
    {"name": "sd",  "code": "sd",  "label": "Sindhi - سنڌي"},
    {"name": "si",  "code": "si",  "label": "Sinhala - සිංහල"},
    {"name": "ta",  "code": "ta",  "label": "Tamil - தமிழ்"},
    {"name": "te",  "code": "te",  "label": "Telugu - తెలుగు"},
    {"name": "ur",  "code": "ur",  "label": "Urdu - اُردُو"},
]

