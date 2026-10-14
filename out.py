"""
Streaming outlier detector over 2D points using a sliding-window
mean/variance check, flagging points whose recent variance collapses
or whose running mean drifts too far from known reference values.
"""
from statistics import mean, variance

data = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]

window_size = 3
MX, VX = 5, 2  # reference mean/variance for the x-coordinate
MY, VY = 10, 1  # reference mean/variance for the y-coordinate

mmx, mmy = [], []  # running means
mvx, mvy = [], []  # sliding window of recent values
outliers = []

for i, (x, y) in enumerate(data):
    if i < window_size:
        mmx.append(x)
        mmy.append(y)
        mvx.append(x)
        mvy.append(y)
    else:
        mmx.append(mean(mvx))
        mmy.append(mean(mvy))
        mvx.append(x)
        mvy.append(y)
        del mvx[0]
        del mvy[0]

    # variance() needs at least 2 points - skip the check until the window has filled
    if len(mvx) < 2:
        continue

    if (variance(mvx) / VX) < 0.05 or (variance(mvy) / VY) < 0.05:
        outliers.append(i)
    elif variance(mvx) == 0 or variance(mvy) == 0:
        outliers.append(i)
    elif (MX - mean(mmx)) > (10 * VX) or (MY - mean(mmy)) > (10 * VY):
        outliers.append(i)

print("Outliers:", outliers)
