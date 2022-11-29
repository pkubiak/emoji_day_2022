import os, json, gzip, glob, datetime
from collections import Counter, defaultdict
import pandas as pd
from utils import chunk
from tqdm import tqdm
from typing import Iterable, Dict
import emoji


def extract_tweets(dir: str, date: str):
    path = os.path.join(dir, f"{date}.jsonl")
    if os.path.exists(path + ".gz"):
        path += ".gz"
    print(f"Opening: {path}")
    with (gzip.open if path.endswith(".gz") else open)(path, "rb") as file:
        for line in file:
            tweet = json.loads(line.decode("utf-8"))
            yield tweet


def collect_available_streams(dir: str = "..\\streams") -> Iterable[str]:
    """Compute list of dates for which we have downloaded streams in `dir` location."""
    dates = set()
    for ext in (".jsonl", ".jsonl.gz"):
        for path in glob.glob(os.path.join(dir, f"*{ext}")):
            print(path)
            date = os.path.basename(path).removesuffix(ext)
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
                dates.add(date)
            except ValueError:
                pass
    print(dates)
    return sorted(dates)


class Collector:
    def __init__(self):
        self.clear()

    def __ilshift__(self, tweets):
        if not isinstance(tweets, list):
            tweets = [tweets]

        self.collect(tweets)

        return self

    def collect(self, tweets: Iterable[Dict]) -> None:
        for tweet in tweets:
            self.collect_tweet(tweet)


class TweetsPerHourCollector(Collector):
    """Count number of Tweets in hourly intervals."""

    def clear(self):
        self.counts = Counter()
        self.seconds = defaultdict(set)

    def collect(self, tweets: Iterable[Dict]) -> None:
        for tweet in tweets:
            hour, rem  = tweet["data"]["created_at"].split(":", maxsplit=1)
            m, s = map(int, rem.split(".")[0].split(":"))
            secs = 60*m+s
            self.counts[hour] += 1
            self.seconds[hour].add(secs)

    def df(self) -> pd.DataFrame:
        return pd.DataFrame(
            [k.split("T") + [v, round(100.0*len(self.seconds[k])/3600, 3)] for k, v in self.counts.items()],
            columns=["Day", "Hour", "Count", "Coverage%"],
        ).sort_values(by=["Day", "Hour"])


class EmojiCounterPerLanguage(Collector):
    """Compute statistics of number of emojis in message per language."""

    def clear(self):
        self.counts = defaultdict(Counter)

    def collect(self, tweets: Iterable[Dict]) -> None:
        for tweet in tweets:
            lang = tweet["data"]["lang"]
            text = tweet["data"]["text"]      
            emojis = emoji.emoji_list(text)
            self.counts[lang][len(emojis)] += 1

    def df(self) -> pd.DataFrame:
        records = []
        for lang in sorted(self.counts, key=lambda k: sum(self.counts[k].values()), reverse=True):
            c = ",".join(f"{k}:{v}" for k,v in sorted(self.counts[lang].items()))
            records.append([lang, c])
        
        return pd.DataFrame(
            records, columns=["Language", "Count"]
        )

class EmojiLocationCollector(Collector):
    def clear(self):
        self.counts = Counter()

    def collect_tweet(self, tweet: Dict) -> None:
        from pprint import pprint
        pprint(tweet)
        assert False
        if tweet["data"]["geo"] and "place_id" in tweet["data"]["geo"]:
            place_id = tweet["data"]["geo"]["place_id"]
            place = [item for item in tweet["includes"]["places"] if item["id"] == place_id]
            assert len(place) == 1
            place = place[0]

            self.counts[place["country"]] += 1
        else:
            self.counts[None] += 1

    def df(self):
        print(self.counts.most_common(100), len(self.counts), sum(self.counts.values()))
# count(key="emoji,lang", "monthly")
# GenericCollector(key="lang,len(emojis)", period="daily")

class TopLanguageEmojis(Collector):
    def __init__(self, top_n: int):
        self.top_n = top_n
    
    def clear(self):
        self.counts = defaultdict(Counter)

    def collect_tweet(self, tweet: Dict) -> None:
        if tweet["data"]["possibly_sensitive"]:
            return

        lang = tweet["data"]["lang"]
        text = tweet["data"]["text"]
        emojis = {i["emoji"] for i in emoji.emoji_list(text)}

        for e in emojis:
            self.counts[lang][e] += 1

    def df(self) -> pd.DataFrame:
        records = []
        for lang in sorted(self.counts, key=lambda k: sum(self.counts[k].values()), reverse=True):
            values = ",".join(f"{k}:{v}" for k,v in self.counts[lang].most_common(self.top_n))
            records.append([lang, values])
        return pd.DataFrame(records, columns=["Language", "Counts"])

class EmojiFrequencyCollector(Collector):
    """Count frequency of Emojis."""

    def clear(self):
        self.counts = Counter()
    
    def collect(self, tweets: Iterable[Dict]) -> None:
        for tweet in tweets:
            text = tweet["data"]["text"]            
            self.counts.update(i["emoji"] for i in emoji.emoji_list(text))

    def df(self) -> pd.DataFrame:
        return pd.DataFrame(
            [[k, v] for k, v in self.counts.most_common()],
            columns=["Emoji", "Count"]
        ).sort_values(by=["Count", "Emoji"], ascending=False)


class FieldStatisticsCollector(Collector):
    def __init__(self, field: str, limit: int = 500):
        super()
        self.field = field.split(".")
        self.limit = limit

    def clear(self):
        self.counts = Counter()

    def collect(self, tweets: Iterable[Dict]) -> None:
        for tweet in tweets:
            value = tweet
            for k in self.field:
                if k not in value:
                    value = None
                    break
                value = value[k]
            
            self.counts[str(value)] += 1
        
    def df(self) -> pd.DataFrame:
        return pd.DataFrame(
            [[k, v] for k, v in self.counts.most_common()],
            columns=["Value", "Count"]
        ).sort_values(by=["Count", "Value"], ascending=False).head(self.limit)
            

if __name__ == "__main__":
    collectors = {
        # "tweets_per_hour": TweetsPerHourCollector(),
        # "emoji_frequency": EmojiFrequencyCollector(),
        # "statistics_lang":  FieldStatisticsCollector("data.lang"),
        # "statistics_source": FieldStatisticsCollector("data.source"),
        # "emoji_lang_frequency": EmojiCounterPerLanguage(),
        # "top_language_emojis": TopLanguageEmojis(1000)
        "test": EmojiLocationCollector(),
    }

    for date in collect_available_streams():
        print("=" * 16, date, "=" * 16)
        current_collectors = {}

        for name, collector in collectors.items():
            collector.clear()
            output_path = os.path.join("..\\data", date, f"{name}.tsv")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            if os.path.exists(output_path):
                print(f"Skipping collecting: {output_path}")
            else:
                current_collectors[output_path] = collector

        if not current_collectors:
            continue

        with tqdm(extract_tweets("..\\streams", date), leave=False) as it:
            try:
                for tweets in chunk(it):
                    for collector in current_collectors.values():
                        collector <<= tweets
            except EOFError as e:
                print(e)
            
        for output_path, collector in current_collectors.items():
            df = collector.df()

            print(f"Saving to {output_path}")
            print(df)
            df.to_csv(output_path, index=False, sep="\t")
            
