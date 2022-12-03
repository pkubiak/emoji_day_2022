from helpers.multi_app import MultiViewsApp


VIEWS = [
    ("🤩 Welcome", "welcome", "welcome.py"),
    
    "Emoji Statistics",
    ("🏆 Most common emojis", "most-common-emojis", "dashboards/01_most_common_emojis.py"),
    ("💗 Top Emojis by category", "top-emojis-by-category", "dashboards/02_top_emojis_by_category.py"),
    ("👫 Gender Bias", "gender-bias", "dashboards/05_gender_bias.py"),
    ("📈 Emoji Trends", "emoji-trends", "dashboards/09_emoji_trends.py"),
    ("📆 Daily Top Emoji", "daily-top-emoji", "dashboards/10_daily_top_emoji.py"),

    "Languages & Countries",
    # ("📈 Language Statistics", "language-statistics", "dashboards/08_language_statistics.py"),
    ("🌍 Top Emojis by language", "top-emojis-by-language", "dashboards/03_top_emojis_by_language.py"),
    ("🥊 Emoji vs Emoji", "emoji-vs-emoji", "dashboards/04_emoji_vs_emoji.py"),

    "Tweets Statistics",
    ("📅 Tweets Count per Date", "tweets-count-per-date", "dashboards/06_tweets_count_per_date.py"),
    ("📩 Attributes statistics", "attributes-statistics", "dashboards/07_attributes_statistics.py"),
    
    "",
    ("🗂️ Glossary", "glossary", "glossary.py"),
    # ("🔧 About Dashboard", "about-dashboard", "placeholder.py"),
]


app = MultiViewsApp(title="Emoji Dashboard", icon="🤣", views=VIEWS)
app.render()