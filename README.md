# Fuzzy Tag Search

Three small Flask microservices built during an internship, each solving the same problem — "find the industrial equipment tags whose description best matches a search string" — with a different string-matching strategy, plus a client script and a standalone outlier detector.

> Originally pointed at an internal company API. The endpoint has been redacted/genericized in this public version — set the `TAG_API_URL` environment variable to point at your own data source to run these.

## Services

| File | Matching strategy |
|---|---|
| `jaccard.py` | Jaccard similarity — overlap between the character sets of the query and each description |
| `lev.py` | Levenshtein (edit) distance |
| `whooshy.py` | Full-text search via the [Whoosh](https://whoosh.readthedocs.io/) index, rebuilt hourly in the background |
| `improved_search.py` | The fixed version: every tag scored with Jaro-Winkler plus abbreviation matching (`matching.py`), cut at a threshold chosen from labeled data |

All three expose the same contract:

```
POST /mytest
{ "searchString": "<query>" }
```

and return a list of `(matching_item, score)` pairs.

## Fixing the first versions

Comparing the three services on the same queries showed three problems in `jaccard.py` and `lev.py`:

1. **They weren't really fuzzy.** Both only scored tags that already contained the exact search string. So searching for `CNDR` could never find `CONDENSER VACUUM`, even though it is the same equipment.
2. **Jaccard ignores letter order.** It compares *sets* of characters, so `DRCN` scored a perfect 1.0, the same as `CNDR`.
3. **Levenshtein measured length.** Every tag that passed the filter contained the query, so the edit distance was just the tag's length minus the query's. Shorter descriptions ranked higher regardless of content.

I fixed these during the internship. That code stayed in ExactSpace's internal systems, so `matching.py` and `improved_search.py` re-implement the fixes for this public repo:

- **Every tag is scored.** There is no exact-substring filter.
- **Scores respect order and abbreviations.** Each query word is matched against each tag word using Jaro-Winkler similarity, which respects letter order and rewards a shared prefix. A word also matches when it is an in-order abbreviation (`CNDR` → `CONDENSER`) or the initials of consecutive words (`BFP` → `BOILER FEED PUMP`).
- **The threshold is chosen from labeled data.** `choose_threshold.py` takes query-tag pairs labeled "same equipment" or not, and reports precision, recall and F1 at each cutoff.

On example tags, for the query `CNDR`:

| Tag description | Before (`lev.py` / `jaccard.py`) | After (`matching.py`) |
|---|---|---|
| CNDR VACUUM | returned | 1.00 |
| CONDENSER VACUUM | **never returned** | 0.90 |
| COND 1 OUTLET TEMP | **never returned** | 0.85 |
| CONDENSATE PUMP DISCHARGE | never returned | 0.72 |
| DRCN | Jaccard 1.00 (if it had passed the filter) | **0.00** |

On the illustrative labeled pairs in `examples/labeled_pairs_example.csv` (written for this repo, not ExactSpace data), the best F1 (0.92) comes from any threshold between 0.715 and 0.85; `improved_search.py` defaults to 0.8. Set `MATCH_THRESHOLD` to whatever `choose_threshold.py` reports for your own labeled pairs.

**Known limitation:** the abbreviation rule can match a different real word that fits the pattern, such as `TUBE` inside `TURBINE`. The labeled-pairs step is how you measure how often that happens on your data.

## Other scripts

- **`client.py`** — minimal client that POSTs a sample query to whichever service is running on port 5000.
- **`out.py`** — a standalone sliding-window outlier detector over 2D points (unrelated to the search services; a separate exercise in streaming anomaly detection using rolling mean/variance).

## Setup

```bash
pip install -r requirements.txt
export TAG_API_URL="http://<your-api-host>/api/tagmeta?filter=..."
python improved_search.py  # or whooshy.py / jaccard.py / lev.py
python client.py           # in another terminal
python test_matching.py    # checks for the three fixes
python choose_threshold.py examples/labeled_pairs_example.csv
```

## Tech stack

Python, Flask, Whoosh, python-Levenshtein, `requests`, `schedule`
