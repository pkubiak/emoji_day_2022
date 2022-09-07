from typing import Iterable, Dict
import glob, json, os
import emoji
import pandas as pd

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
    html += ['<table style="table-layout:fixed;width:100%;empty-cells:hide;">']
    for row in range((len(items)+n_cols-1) // n_cols):
        html += ["<tr>"]
        for col in range(n_cols):
            i = n_cols*row + col
            if i >= len(items):
                html += ['<td></td>']
                continue
            value = items[i][1]
            if type(value) == int:
                value = f"{value:,d}"
            else:
                value = "<0.001%" if value < 0.001 else f"{value:.3f}%"
            html += [f"<td title='{emoji.demojize(items[i][0])}'>{items[i][0]}<span style='float:right'>{value}</span></td>"]
        html += ["</tr>"]
    html += ["</table>"]

    return "\n".join(html)

def get_tsv_data(key: str, **kwargs):
    dfs = []
    for path in glob.glob(os.path.join(os.path.dirname(__file__), "data","*",f"{key}.tsv")):
        print(os.path.abspath(path))
        df = pd.read_csv(path, sep="\t", **kwargs)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)
    

def chunk(items, chunk_size: int = 1000):
    cache = []
    for item in items:
        if len(cache) == chunk_size:
            yield cache
            cache = []
        cache.append(item)

    yield cache