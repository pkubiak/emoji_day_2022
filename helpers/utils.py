from typing import Iterable, Dict
import glob, json, os
import pandas as pd
from functools import reduce


Tweet = Dict

def iteratate_tweets(dirname: str, limit: int = 10000000000) -> Iterable[Tweet]:
    dirname = os.path.join(os.path.abspath(dirname), "*.jsonl")
    print(dirname)

    for path in sorted([]):
        with open(path,"r",encoding="utf-8") as file:
            print(path)
            ile = 0
            for line in file:
                tweet = json.loads(line)
                yield tweet
                ile += 1
                if ile >= limit:
                    break
            print(path, ile)


def iterate_dates_range(start: str, end: str, as_str: bool = True) -> Iterable[str]:
    from datetime import datetime, timedelta
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    assert start <= end

    i = 0
    while True:
        yield start.strftime("%Y-%m-%d") if as_str else start
        if start == end: break
        start += timedelta(days=1)


def render_as_table(items, n_cols: int = 6, limit: int = None) -> str:
    # items = list(items.most_common())
    # if limit:
    #     items = items[:limit]
    
    html = [
        "<style>td:hover{background:#eee}</style>"
    ]
    html += ['<table style="table-layout:fixed;width:100%;empty-cells:hide;" class="emoji">']
    for row in range((len(items)+n_cols-1) // n_cols):
        html += ["<tr>"]
        for col in range(n_cols):
            i = n_cols*row + col
            if i >= len(items):
                html += ['<td></td>']
                continue
            key, value, *title = items[i]
            title = f" title={repr(title[0])}" if title else ""

            if type(value) == int:
                value = f"{value:,d}"
            elif type(value) == float:
                value = "<0.001%" if value < 0.001 else f"{value:.3f}%"

            html += [f"<td{title}>{key}<span style='float:right'>{value}</span></td>"]
        html += ["</tr>"]
    html += ["</table>"]

    return "\n".join(html)

def get_tsv_data(key: str, with_dates=False, **kwargs) -> Iterable[pd.DataFrame]:
    for path in glob.glob(os.path.join(os.path.dirname(__file__), "..", "data","*",f"{key}.tsv")):
        df = pd.read_csv(path, sep="\t", **kwargs)
        if with_dates:
            date = path.split(os.sep)[-2]
            yield date, df
        else:
            yield df
    # return pd.concat(dfs, ignore_index=True)


def sum_tsv_data(key: str, **kwargs):
    data = get_tsv_data(key, **kwargs)

    # ref: https://stackoverflow.com/a/38472352/5822988
    df = reduce(lambda a, b: a.add(b, fill_value=0), data)
    return df
    

def chunk(items, chunk_size: int = 1000):
    cache = []
    for item in items:
        if len(cache) == chunk_size:
            yield cache
            cache = []
        cache.append(item)

    yield cache

def normalize_emoji(e: str) -> str:
    for c in [0x1F3FB,0x1F3FC,0x1F3FD,0x1F3FE,0x1F3FF,0xFE0F]:
        e = e.replace(chr(c), "")
    
    e = e.removesuffix("\u200d\u2640")
    e = e.removesuffix("\u200d\u2642")
    return e
