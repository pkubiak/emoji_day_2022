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


def collect_available_streams(dir: str = "streams") -> Iterable[str]:
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
    return sorted(dates)


class Collector:
    def __init__(self):
        self.clear()

    def __ilshift__(self, tweets):
        if not isinstance(tweets, list):
            tweets = [tweets]

        self.collect(tweets)

        return self


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


class EmojiFrequenceCollector(Collector):
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
        "tweets_per_hour": TweetsPerHourCollector(),
        "emoji_frequency": EmojiFrequenceCollector(),
        "statistics_lang":  FieldStatisticsCollector("data.lang"),
        "statistics_source": FieldStatisticsCollector("data.source"),
    }

    for date in collect_available_streams():
        print("=" * 16, date, "=" * 16)
        current_collectors = {}

        for name, collector in collectors.items():
            collector.clear()
            output_path = os.path.join("data", date, f"{name}.tsv")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            if os.path.exists(output_path):
                print(f"Skipping collecting: {output_path}")
            else:
                current_collectors[output_path] = collector

        if not current_collectors:
            continue

        with tqdm(extract_tweets("streams", date), leave=False) as it:
            for tweets in chunk(it):
                for collector in current_collectors.values():
                    collector <<= tweets

        for output_path, collector in current_collectors.items():
            df = collector.df()

            print(f"Saving to {output_path}")
            print(df)
            df.to_csv(output_path, index=False, sep="\t")
            