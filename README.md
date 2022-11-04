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

## 💪 Checklist
- [x] Create own system for multipage dashobard:
    - [x] Support custom menu building
    - [x] Allows to navigate views with buttons
- [x] Implement constant collection of Twitter logs
    - [x] using vm on Google Cloud Engine
- [ ] Prepare analytical dashboards:
    - [ ] Emoji Statistic:
        - [x] Overall most common emojis
        - [x] Most common emoji by categories (faces, animals, etc.)
        - [ ] 👷 Gender bias analysis
    - [ ] Language correlations: 
        - [x] Most common emoji in each category by language
        - [x] Comparison of two emojis popularity on map
        - [ ] 👷‍♀️ Number of emoji per tweet by language
    - [ ] Tweets Statistics:
        - [x] Number of collected tweets per date
        - [ ] 👷‍♀️ Histogram of values for different tweets parameters (language, source, etc.)
- [ ] 👷‍♀️ Prepare glossary