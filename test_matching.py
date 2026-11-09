"""Checks for the three fixes in matching.py. Run: python test_matching.py"""
from matching import match_score, search

# 1. Tags that don't contain the exact query are still found
assert match_score("CNDR", "CONDENSER VACUUM") >= 0.85
assert match_score("CNDR", "COND 1 OUTLET TEMP") >= 0.8

# 2. Character order matters: "DRCN" is not "CNDR"
assert match_score("CNDR", "DRCN") < 0.5

# 3. Longer descriptions are not penalized for their length
assert match_score("CNDR", "CNDR-1 OUTLET TEMP") == match_score("CNDR", "CNDR")

# Acronyms match the initials of consecutive words
assert match_score("BFP", "BOILER FEED PUMP A") >= 0.85

# Multi-word queries match abbreviated tags
assert match_score("BOILER FEED PUMP", "BLR FD PMP A") >= 0.85

tags = [{"description": d} for d in ["CONDENSER VACUUM", "DRCN", "COOLING TOWER FAN", "CNDR VACUUM"]]
found = [t["description"] for t, _ in search("CNDR", tags, threshold=0.8)]
assert found == ["CNDR VACUUM", "CONDENSER VACUUM"], found

print("All checks passed")
