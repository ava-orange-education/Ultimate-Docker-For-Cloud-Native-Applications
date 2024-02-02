"""
The following source code is taken from the following URL:
https://iqss.github.io/dss-rce/batch-job-examples.html#python-1
"""

import os
import random
import sys

from scipy import stats


def sim_ttest(mu1, mu2, sd, n1, n2):
    x = stats.norm.rvs(loc=mu1, scale=sd, size=n1)
    y = stats.norm.rvs(loc=mu2, scale=sd, size=n2)
    return stats.ttest_ind(x, y)[1]


nsims = int(os.getenv("NUM_SIMULATIONS", 1_000))
p = [sim_ttest(1, 1.3, 1, 50, 150) for x in range(nsims)]

# hostname + pid
me = os.uname()[1] + "-" + str(os.getpid())
result = len([x for x in p if x < 0.05]) / nsims

data_dir = os.getenv("DATA_DIR", "/tmp")

with open(f"{data_dir}/result-" + me, "w") as f:
    f.write(str(result))

if random.random() > 0.5:
    print("Some error occurred", file=sys.stderr, flush=True)
    exit(1)
else:
    print("Success", flush=True)
    exit(0)
