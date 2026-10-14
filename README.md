# Fuzzy Tag Search

Three small Flask microservices built during an internship, each solving the same problem — "find the industrial equipment tags whose description best matches a search string" — with a different string-matching strategy, plus a client script and a standalone outlier detector.

> Originally pointed at an internal company API. The endpoint has been redacted/genericized in this public version — set the `TAG_API_URL` environment variable to point at your own data source to run these.

## Services

| File | Matching strategy |
|---|---|
| `jaccard.py` | Jaccard similarity — overlap between the character sets of the query and each description |
| `lev.py` | Levenshtein (edit) distance |
| `whooshy.py` | Full-text search via the [Whoosh](https://whoosh.readthedocs.io/) index, rebuilt hourly in the background |

All three expose the same contract:

```
POST /mytest
{ "searchString": "<query>" }
```

and return a list of `(matching_item, score)` pairs.

## Other scripts

- **`client.py`** — minimal client that POSTs a sample query to whichever service is running on port 5000.
- **`out.py`** — a standalone sliding-window outlier detector over 2D points (unrelated to the search services; a separate exercise in streaming anomaly detection using rolling mean/variance).

## Setup

```bash
pip install -r requirements.txt
export TAG_API_URL="http://<your-api-host>/api/tagmeta?filter=..."
python whooshy.py          # or jaccard.py / lev.py
python client.py           # in another terminal
```

## Tech stack

Python, Flask, Whoosh, python-Levenshtein, `requests`, `schedule`
