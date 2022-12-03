# Twitter Emoji Dashboard

To celebrate Emoji Day 2022, I decided to create some analytical dashboard about Emojis.


## 🎯 Personal goals
- Learn Google Cloud Engine,
- Deepen knowledge about Streamlit,
- Conduct interesting analyses with lots of data

## 🏭 How it works?

1. Python script collects Tweets using Twitter API and dump them into `.jsonl.gz` file:
    - script source: `helpers/twitter.py`,
    - into compressed JSONL file,
    - runs on Google Cloud

2. Interesting data is extracted from dumps using Data Extractors and dumped into `.tsv` files:
    - data extractors are defined in `helpers/data_extractors.py`,
    - dumps are stored in `data/YYYY-MM-DD/` directories,

3. Interactive dashboards are created using streamlit:
    - dashboards are implemented in `views/dashboards/` directory,
    - dashboard use already precomputed data from `.tsv` dumps,
    - dashboards are attached to the main application in `main.py` file
    - python module `emoji` is used to manipulate emojis in strings
    - in client browser missing emojis are rendered using `Noto Emoji` font from https://fonts.google.com/


## 💡 Further Ideas

- [ ] Add more emoji to gender bias visualisation
- [ ] Daily Top emoji ranking
- [ ] How often emojis are used in different languages / countries
- [ ] Emoji n-grams 
- [ ] Emoji co-occurences
- [ ] Emojis from different standards