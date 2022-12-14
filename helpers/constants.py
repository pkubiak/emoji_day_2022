import emoji
from helpers.utils import normalize_emoji


CATEGORIES = {
    "birds": "๐ฆ,๐,๐,๐ฃ,๐ค,๐ฅ,๐ฆ,๐ง,๐๏ธ,๐ฆ,๐ฆ,๐ฆ,๐ฆฉ,๐ชถ,๐ฆค,๐ฆ,๐ฆข,๐ฆ,๐ชฟ,๐ฆโโฌ,๐ฆค",
    "marine": "๐ณ,๐,๐ฌ,๐ฆญ,๐,๐ ,๐ก,๐ฆ,๐,๐,๐ชธ,๐ชผ,๐ฆญ,๐ชธ",
    "flowers": "๐,๐ธ,๐ฎ,๐ชท,๐ต๏ธ,๐น,๐ฅ,๐บ,๐ป,๐ผ,๐ท,๐ชป,๐ชด,๐ชท",
    "fruits": "๐,๐,๐,๐,๐,๐,๐,๐ฅญ,๐,๐,๐,๐,๐,๐,๐ซ,๐ฅ,๐,๐ซ,๐ฅฅ,๐ซ,๐ซ",
    "vegetables": "๐ฅ,๐,๐ฅ,๐ฅ,๐ฝ,๐ถ๏ธ,๐ซ,๐ฅ,๐ฅฌ,๐ฅฆ,๐ง,๐ง,๐,๐ฅ,๐ซ,๐ฐ,๐ซ,๐ซ,๐ซ,๐ซ",
    "mammals": "๐ต,๐,๐ฆ,๐ฆง,๐ถ,๐,๐ฆฎ,๐โ๐ฆบ,๐ฉ,๐บ,๐ด,๐,๐,๐ฏ,๐ฆ,๐โโฌ,๐,๐ฑ,๐ฆ,๐ฆ,๐,๐ฆ,๐ฆ,๐ฆ,๐ฆฌ,๐ฎ,๐,๐,๐,๐ท,๐,๐,๐ฝ,๐,๐,๐,๐ช,๐ซ,๐ฆ,๐ฆ,๐,๐ฐ,๐น,๐,๐,๐ญ,๐ฆ,๐ฆ,๐ฆฃ,๐,๐ฟ๏ธ,๐ฆซ,๐ฆ,๐ฆ,๐ป,๐ปโโ๏ธ,๐จ,๐ผ,๐ฆฅ,๐ฆฆ,๐พ,๐ฆก,๐ฆ,๐ฆจ,๐ซ,๐ซ,๐ฆซ,๐ฆฌ",
    # "watches": "๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐ ,๐ก,๐ข,๐ฃ,๐ค,๐ฅ,๐ฆ,๐ง",
    "numbers": "0๏ธโฃ,1๏ธโฃ,2๏ธโฃ,3๏ธโฃ,4๏ธโฃ,5๏ธโฃ,6๏ธโฃ,7๏ธโฃ,8๏ธโฃ,9๏ธโฃ,๐",
    "weather": "โ๏ธ,๐ค,โ๏ธ,๐ฅ,โ๏ธ,๐ฆ,๐ง,โ,๐ฉ,๐จ,โ๏ธ",
    "moons": "๐,๐,๐,๐,๐,๐,๐,๐",
    "shoes": "๐,๐,๐ฅพ,๐ฅฟ,๐ ,๐ก,๐ฉฐ,๐ข,๐ฉด,๐ผ,โธ๏ธ",
    "zodiacs": "โ,โ,โ,โ,โ,โ,โ,โ,โ,โ,โ,โ,โ",
    "sports": "โฝ,โพ,๐ฅ,๐,๐,๐,๐,๐พ,๐ฅ,๐ณ,๐,๐,๐,๐ฅ,๐,๐ธ,๐ฅ,๐ฅ,๐ฅ,โณ,โธ,๐ฃ,๐คฟ,๐ฝ,๐ฟ,๐ท,๐ฅ",
    "religious": "โช,๐,๐,๐,โฉ,๐",
    "plants": "๐ฑ,๐ชด,๐ฒ,๐ณ,๐ด,๐ต,๐พ,๐ฟ,โ,๐,๐,๐,๐,๐ชน,๐ชบ,๐",
    "asian_food": "๐ฑ,๐,๐,๐,๐,๐,๐,๐ ,๐ข,๐ฃ,๐ค,๐ฅ,๐ฅฎ,๐ก,๐ฅ,๐ฅ ,๐ฅก",
    "drinks": "๐ผ,๐ฅ,โ,๐ซ,๐ต,๐ถ,๐พ,๐ท,๐ธ,๐น,๐บ,๐ป,๐ฅ,๐ฅ,๐ซ,๐ฅค,๐ง,๐ง,๐ง,๐ซ,๐ง",
    "books": "๐,๐,๐,๐,๐,๐,๐",
    "insects": "๐ชฒ,๐,๐,๐ฆ,๐ฆ,๐ชฐ,๐ชณ,๐ชฑ,๐,๐,๐ฆ"
}

# CATEGORIES = {
#     k: ",".join(normalize_emoji(e) for e in v.split(","))
#     for k, v in CATEGORIES.items()
# }

def get_by_keyword(keywords: str, verbose=False, ignore=[]) -> str:
    if isinstance(keywords, str):
        keywords = [keywords]

    emojis = set()
    for k,v in emoji.EMOJI_DATA.items():
        key = v.get("alias",[]) + [v.get("en","")]
        key = ";".join(f"_{v.strip(':')}_" for v in key)
        if any(k in key for k in keywords) and not any(k in key for k in ignore):
            if verbose:
                print(k, v)
            emojis.add(normalize_emoji(k))
    return ",".join(emojis)

CATEGORIES["countries"] = get_by_keyword("flag_for")
CATEGORIES["circles"] = get_by_keyword("_circle_", ignore=["record"])
CATEGORIES["faces"] = get_by_keyword("_face_") + ",๐คฃ,๐คฉ,๐คฏ"
CATEGORIES["medals"] = get_by_keyword("medal")
CATEGORIES["family"] = get_by_keyword("family")
CATEGORIES["hands"] = get_by_keyword(["thumb", "_hand_","finger"], ignore=["hand_over_mouth", "raising_hand", "tipping_hand"])
CATEGORIES["hearts"] = get_by_keyword("heart", ignore=["couple", "smiling", "heart_hands", "folding_hand_fan"])
CATEGORIES["squares"] = get_by_keyword("square", ignore=["button", "small", "medium"])
CATEGORIES["watches"] = get_by_keyword("clock", verbose=True, ignore=["button", "arrows"])


LANG_TO_COUNTRY = {
    "pl": "POL",
    "ja": "JPN",
    "de": "DEU",
    "fr": "FRA",
    "it": "ITA",
    "ko": "KOR",
    "es": "ESP",
    "cs": "CZE",
    "uk": "UKR",
    "is": "ISL",
    "pt": "PRT",
    "tl": "PHL",
    "ru": "RUS",
    "no": "NOR",
    "lt": "LTU",
    "lv": "LVA",
    "am": "ETH",
    "sl": "SVN",
    "sk": "SVK",
    "et": "EST",
    "nl": "NLD",
    "ht": "HTI",
    "vi": "VNM",
    "hu": "HUN",
    "en": ["USA", "GBR"],
    "el": "GRC",
    "tr": "TUR",
    "zh": "CHN",
    "sr": "SRB",
    "da": "DNK",
    "ro": "ROU",
    "bg": "BGR",
    "sq": "ALB",
    # "hr": "HRV",
}