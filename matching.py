"""
Order-aware fuzzy matching for equipment tag descriptions.

Fixes three problems in the first versions (jaccard.py, lev.py):

1. They only scored tags that already contained the exact search string, so
   a query like "CNDR" could never find "CONDENSER VACUUM". Here every tag is
   scored.
2. Jaccard compared sets of characters, so "CNDR" and "DRCN" looked
   identical. Every score here respects character order.
3. Raw Levenshtein distance grew with description length, so it ranked long
   descriptions lower regardless of content. Here each query is compared
   word by word with Jaro-Winkler similarity, which is already 0-1.

Plant tags are full of abbreviations ("CNDR" for condenser, "TEMP" for
temperature), so a word also matches when the query is an in-order
abbreviation of it: same first letter, and every query letter appears in the
word in the same order. A query word also matches the initials of consecutive
words ("BFP" for "BOILER FEED PUMP").

Known limitation: the abbreviation rule can match a different real word that
happens to fit the pattern, such as "TUBE" inside "TURBINE". Choosing the
threshold from labeled pairs (choose_threshold.py) measures how often that
happens on your data.
"""
import re


def normalize(text):
    """Upper-case and split into words, treating punctuation as a separator."""
    return re.findall(r"[A-Z0-9]+", text.upper())


def jaro_winkler(a, b, prefix_scale=0.1):
    """Jaro-Winkler similarity: order-aware, and rewards a shared prefix."""
    if a == b:
        return 1.0
    if not a or not b:
        return 0.0
    window = max(max(len(a), len(b)) // 2 - 1, 0)
    a_match, b_match = [False] * len(a), [False] * len(b)
    matches = 0
    for i, ca in enumerate(a):
        for j in range(max(0, i - window), min(len(b), i + window + 1)):
            if not b_match[j] and b[j] == ca:
                a_match[i] = b_match[j] = True
                matches += 1
                break
    if not matches:
        return 0.0
    a_seq = [c for c, m in zip(a, a_match) if m]
    b_seq = [c for c, m in zip(b, b_match) if m]
    transpositions = sum(x != y for x, y in zip(a_seq, b_seq)) / 2
    jaro = (matches / len(a) + matches / len(b) + (matches - transpositions) / matches) / 3
    prefix = 0
    for x, y in zip(a[:4], b[:4]):
        if x != y:
            break
        prefix += 1
    return jaro + prefix * prefix_scale * (1 - jaro)


def is_abbreviation(short, word):
    """True if `short` abbreviates `word`: same first letter, and its letters appear in `word` in order."""
    if len(short) < 2 or len(short) >= len(word) or short[0] != word[0]:
        return False
    it = iter(word)
    return all(ch in it for ch in short)


def word_score(query_word, tag_word):
    if query_word == tag_word:
        return 1.0
    if is_abbreviation(query_word, tag_word) or is_abbreviation(tag_word, query_word):
        return 0.9
    return jaro_winkler(query_word, tag_word)


def is_acronym(short, words):
    """True if `short` is the initials of consecutive words, like "BFP" for "BOILER FEED PUMP"."""
    n = len(short)
    return n >= 2 and any("".join(w[0] for w in words[i:i + n]) == short for i in range(len(words) - n + 1))


def match_score(query, description):
    """Average, over the query's words, of each word's best match in the description (0 to 1)."""
    q_words, d_words = normalize(query), normalize(description)
    if not q_words or not d_words:
        return 0.0
    return sum(0.9 if is_acronym(q, d_words) else max(word_score(q, d) for d in d_words) for q in q_words) / len(q_words)


def search(query, tags, threshold):
    """Score every tag and return those at or above the threshold, best first."""
    scored = [(tag, round(match_score(query, tag["description"]), 3)) for tag in tags]
    return sorted([s for s in scored if s[1] >= threshold], key=lambda s: s[1], reverse=True)
