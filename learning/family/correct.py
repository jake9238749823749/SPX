"""Family-wise correction for N trials. Usage: python3 correct.py N [T_obs] [SR_var]
Reports Bonferroni and Holm thresholds on a z-score, and the deflated-Sharpe expected maximum (SR0) for N trials.
SR0 uses the Bailey & Lopez de Prado (2014) expected-maximum formula. T_obs = number of return observations, SR_var = variance of trial Sharpe ratios (per period)."""
import sys
from statistics import NormalDist
from math import sqrt, log
N = int(sys.argv[1]); T = int(sys.argv[2]) if len(sys.argv) > 2 else 252 * 3; V = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5 / 252
nd = NormalDist(); g = 0.5772156649
alpha = 0.05
print(f'N trials = {N}')
print(f'Bonferroni: per-test p < {alpha/N:.2e}, z > {nd.inv_cdf(1-alpha/(2*N)):.2f} (two-sided)')
print(f'Holm: strictest step is the same as Bonferroni; the k-th smallest p must be < alpha/(N-k+1)')
SR0 = sqrt(V) * ((1 - g) * nd.inv_cdf(1 - 1/N) + g * nd.inv_cdf(1 - 1/(N * 2.718281828)))
print(f'Expected max Sharpe under pure chance (per period): {SR0:.4f}  = {SR0*sqrt(252):.2f} annualised')
print(f'A period Sharpe must exceed this to beat the family, and the deflated Sharpe must be > 0.95 to pass.')
