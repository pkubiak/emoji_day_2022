import json
import logging
import os
import sys
import traceback
from contextlib import ExitStack
import gzip
import time
import requests
from tqdm import tqdm


logging.getLogger().setLevel(logging.INFO)

BEARER_TOKEN = os.environ["BEARER_TOKEN"]


class KeyedWriter:
    def __init__(self, dir: str, compress: bool = False):
        if not os.path.exists(dir):
            os.makedirs(dir)
        assert os.path.isdir(dir)
        self._compress = compress
        self._dir = dir
        self._handlers = dict()
    
    def __enter__(self):
        self._stack = ExitStack()
        return self

    def __exit__(self, *exc):
        self._stack.close()

    def __getitem__(self, key: str):
        try:
            return self._handlers[key]
        except KeyError:
            output_path = os.path.join(self._dir, key)
            if self._compress:
                output_path += '.gz'

            logging.info("Opening new file: %s", output_path)
            h = (gzip.open if self._compress else open)(output_path, "ab")
            self._stack.enter_context(h)
            self._handlers[key] = h
            return h


def bearer_oauth(r):
    """Method required by bearer token authentication."""
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2SampleStreamPython"
    return r



def get_stream(output_dir: str):
    """Collect all available tweets with details."""
    # ref: https://developer.twitter.com/en/docs/twitter-api/tweets/volume-streams/api-reference/get-tweets-sample-stream
    request = requests.get(
        "https://api.twitter.com/2/tweets/sample/stream?", auth=bearer_oauth, stream=True, timeout=(10, 20),
        params={
            "tweet.fields": ",".join([
                "attachments", 
                "author_id", "context_annotations", "conversation_id", "created_at",
                "entities", "geo", "id", "in_reply_to_user_id", "lang", "source",
                "possibly_sensitive", "text", "referenced_tweets",
            ]),
            "expansions": ",".join([
                "attachments.poll_ids", "attachments.media_keys", "author_id", "entities.mentions.username", "geo.place_id", "in_reply_to_user_id"
            ]),
            "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
            "user.fields": "created_at,description,location,name,protected,public_metrics,username,verified",
            "media.fields": "type,alt_text"
        }
    )

    with request as response:
        if response.status_code != 200:
            print(response.status_code, response.text, response.headers)
        if response.status_code == 429:
            time.sleep(60)
        assert response.ok

        with KeyedWriter(output_dir, compress=True) as output, tqdm(response.iter_lines(), smoothing=0.04) as progress:
            for response_line in progress:
                if not response_line: continue
                json_response = json.loads(response_line)

                key = json_response["data"]["created_at"].split("T")[0] + ".jsonl"
                output[key].write(response_line + b"\n")


if __name__ == "__main__":
    while True:
        try:
            get_stream(sys.argv[1])
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
        time.sleep(5)