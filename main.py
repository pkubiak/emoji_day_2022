from helpers.multi_app import MultiViewsApp


VIEWS = [
    ("🤩 Welcome", "welcome", "placeholder.py"),
    
    "Emoji Statistics",
    ("🏆 Most common emojis", "most-common-emojis", "dashboards/01_most_common_emojis.py"),
    ("💗 Top Emojis by category", "top-emojis-by-category", "dashboards/02_top_emojis_by_category.py"),
    ("\uFE0F♂️\uFE0F vs ♀️\uFE0F", "gender-bias", "dashboards/05_gender_bias.py"),

    "Per Language",
    ("🌍 Top Emojis by country", "top-by-country-and-language", "dashboards/03_top_emojis_by_category_and_language.py"),
    ("🥊 Emoji vs Emoji", "emoji-vs-emoji", "dashboards/04_emoji_vs_emoji.py"),

    "Tweets Statistics",
    ("📅 Tweets Count per Date", "tweets-count-per-date", "dashboards/06_tweets_count_per_date.py"),
    ("📩 Attributes statistics", "attributes-statistics", "dashboards/07_attributes_statistics.py"),
    
    "",
    ("🗂️ Glossary", "glossary", "glossary.py"),
    ("🔧 About Dashboard", "about-dashboard", "placeholder.py"),
]


app = MultiViewsApp(title="Emoji Dashboard", icon="🤣", views=VIEWS)
app.render()