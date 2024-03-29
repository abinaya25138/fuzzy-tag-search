from statistics import mean, variance
import numpy as np

data = [[1,2], [3,4], [5,6], [7,8], [9,10]]

window_size = 3
MX = 5
VX = 2
MY = 10
VY = 1

mmx = []
mmy = []
mvx = []
mvy = []
outliers = []

for i, point in enumerate(data):
    x = point[0]
    y = point[1]
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
    if (variance(mvx) / VX) < 0.05 or (variance(mvy) / VY) < 0.05:
        outliers.append(i)
    elif variance(mvx) == 0 or variance(mvy) == 0:
        outliers.append(i)
    elif (MX - mean(mmx)) > (10 * VX) or (MY - mean(mmy)) > (10 * VY):
        outliers.append(i)

print("Outliers:", outliers)

