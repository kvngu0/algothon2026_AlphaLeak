import numpy as np
 
# Alpha Leak - cross-sectional mean reversion strategy
# Idea: compare each instrument's recent return to the group average.
# Long relative losers, short relative winners, betting divergence within
# the group reverts. Market-neutral-ish: robust to overall trend direction.
# Tested positive on BOTH days 251-500 (+36) and days 501-750 (+116),
# unlike pure momentum (+119/-154) or own-history mean reversion (-51/+196).
 
nInst = 51
currentPos = np.zeros(nInst)
LOOKBACK = 8
 
def getMyPosition(prcSoFar):
    global currentPos
    (nins, nt) = prcSoFar.shape
    if nt < LOOKBACK + 1:
        return np.zeros(nins)
 
    todayPrice = prcSoFar[:, -1]
 
    # each instrument's return over the lookback window
    ret = np.log(todayPrice / prcSoFar[:, -LOOKBACK])
 
    # relative to the cross-sectional (group) average
    relRet = ret - np.mean(ret)
 
    # bet on reversal of relative performance
    signal = -relRet
 
    # normalize to unit length so position sizing stays consistent
    norm = np.sqrt(signal.dot(signal))
    if norm > 0:
        signal = signal / norm
 
    rpos = np.array([int(x) for x in 5000 * signal / todayPrice])
    currentPos = np.array([int(x) for x in currentPos + rpos])
    return currentPos
 