import emoji
from helpers.utils import normalize_emoji


CATEGORIES = {
    "hearts": "💘,💝,💖,💗,💓,💞,💕,💟,❣️,💔,❤️‍🔥,❤️‍🩹,❤️,🧡,💛,💚,🤎,💙,💜,🖤,🤍,🫀,♥️",
    "birds": "🦃,🐔,🐓,🐣,🐤,🐥,🐦,🐧,🕊️,🦅,🦜,🦚,🦩,🪶,🦤,🦉,🦢,🦆",
    "marine": "🐳,🐋,🐬,🦭,🐟,🐠,🐡,🦈,🐙,🐚,🪸",
    "flowers": "💐,🌸,💮,🪷,🏵️,🌹,🥀,🌺,🌻,🌼,🌷",
    "fruits": "🍇,🍈,🍉,🍊,🍋,🍌,🍍,🥭,🍎,🍏,🍐,🍑,🍒,🍓,🫐,🥝,🍅,🫒,🥥",
    "vegetables": "🥑,🍆,🥔,🥕,🌽,🌶️,🫑,🥒,🥬,🥦,🧄,🧅,🍄,🥜,🫘,🌰",
    "mammals": "🐵,🐒,🦍,🦧,🐶,🐕,🦮,🐕‍🦺,🐩,🐺,🐴,🐆,🐅,🐯,🦁,🐈‍⬛,🐈,🐱,🦝,🦊,🐎,🦄,🦓,🦌,🦬,🐮,🐂,🐃,🐄,🐷,🐖,🐗,🐽,🐏,🐑,🐐,🐪,🐫,🦙,🦒,🐇,🐰,🐹,🐀,🐁,🐭,🦛,🦏,🦣,🐘,🐿️,🦫,🦔,🦇,🐻,🐻‍❄️,🐨,🐼,🦥,🦦,🐾,🦡,🦘,🦨",
    "squares": "🟥,🟧,🟨,🟩,🟦,🟪,⬛,⬜,🟫",
    "watches": "🕐,🕑,🕒,🕓,🕔,🕕,🕖,🕗,🕘,🕙,🕚,🕛,🕜,🕝,🕞,🕟,🕠,🕡,🕢,🕣,🕤,🕥,🕦,🕧",
    "numbers": "0️⃣,1️⃣,2️⃣,3️⃣,4️⃣,5️⃣,6️⃣,7️⃣,8️⃣,9️⃣,🔟",
    "weather": "☀️,🌤,⛅️,🌥,☁️,🌦,🌧,⛈,🌩,🌨,❄️",
    "moons": "🌕,🌖,🌗,🌘,🌑,🌒,🌓,🌔",
    "shoes": "👞,👟,🥾,🥿,👠,👡,🩰,👢",
    "zodiacs": "♈,♉,♊,♋,♌,♍,♎,♏,♐,♑,♒,♓,⛎",
    "sports": "⚽,⚾,🥎,🏀,🏐,🏈,🏉,🎾,🥏,🎳,🏏,🏑,🏒,🥍,🏓,🏸,🥊,🥋,🥅,⛳,⛸,🎣,🤿,🎽,🎿,🛷,🥌",
    "religious": "⛪,🕌,🛕,🕍,⛩,🕋",
    "plants": "🌱,🪴,🌲,🌳,🌴,🌵,🌾,🌿,☘,🍀,🍁,🍂,🍃,🪹,🪺,🍄",
    "asian_food": "🍱,🍘,🍙,🍚,🍛,🍜,🍝,🍠,🍢,🍣,🍤,🍥,🥮,🍡,🥟,🥠,🥡",
    "drinks": "🍼,🥛,☕,🫖,🍵,🍶,🍾,🍷,🍸,🍹,🍺,🍻,🥂,🥃,🫗,🥤,🧋,🧃,🧉",
    "books": "📕,📘,📙,📓,📗,📔,📒",
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
                print(v)
            emojis.add(k)
    return ",".join(emojis)

CATEGORIES["countries"] = get_by_keyword("flag_for")
CATEGORIES["circles"] = get_by_keyword("_circle_", ignore=["record"])
CATEGORIES["faces"] = get_by_keyword("_face_") + ",🤣,🤩,🤯"
# print(CATEGORIES["faces"])
CATEGORIES["medals"] = get_by_keyword("medal")
CATEGORIES["family"] = get_by_keyword("family")
# print(CATEGORIES["family"])
CATEGORIES["hands"] = get_by_keyword(["thumb", "_hand_"], ignore=["hand_over_mouth", "raising_hand", "tipping_hand"])


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