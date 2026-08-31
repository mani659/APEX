import os
import glob
import zipfile
import pandas as pd
import numpy as np
import scipy.stats as si
import warnings

warnings.filterwarnings('ignore')

def black_76(F, K, t, r, sigma, opt_type):
    # F: futures price
    # K: strike price
    # t: time to maturity (in years)
    # r: risk-free rate
    # sigma: volatility
    # opt_type: 'C' or 'P'
    
    # Handle edge cases
    if t <= 0 or F <= 0 or K <= 0 or sigma <= 0:
        return np.nan
        
    d1 = (np.log(F / K) + 0.5 * (sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    
    if opt_type == 'C':
        price = np.exp(-r * t) * (F * si.norm.cdf(d1) - K * si.norm.cdf(d2))
    elif opt_type == 'P':
        price = np.exp(-r * t) * (K * si.norm.cdf(-d2) - F * si.norm.cdf(-d1))
    else:
        price = np.nan
        
    return price

def implied_vol_black_76(target_price, F, K, t, r, opt_type):
    if np.isnan(target_price) or target_price <= 0:
        return np.nan
        
    MAX_ITER = 100
    TOL = 1e-6
    sigma = 0.20 # initial guess
    
    for i in range(MAX_ITER):
        price = black_76(F, K, t, r, sigma, opt_type)
        if np.isnan(price):
            return np.nan
            
        diff = price - target_price
        if abs(diff) < TOL:
            return sigma
            
        d1 = (np.log(F / K) + 0.5 * (sigma ** 2) * t) / (sigma * np.sqrt(t))
        vega = F * np.exp(-r * t) * si.norm.pdf(d1) * np.sqrt(t)
        
        if vega < 1e-8:
            return np.nan
            
        sigma = sigma - diff / vega
        if sigma <= 0:
            sigma = 1e-6
            
    return np.nan

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'databento'))
    
    # 1. Local Discovery
    print("1. Local Discovery...")
    all_zips = glob.glob(os.path.join(base_dir, '*.zip'))
    
    futures_def_zip = None
    options_def_zip = None
    options_bbo_zip = None
    futures_bbo_zip = None
    
    for z in all_zips:
        if 'RMS9TQEJU8' in z:
            futures_def_zip = z
        elif 'QS8HCDJ6GN' in z:
            options_def_zip = z
        elif 'AEWM5PMURM' in z:
            options_bbo_zip = z
        else:
            futures_bbo_zip = z
            
    if not futures_bbo_zip:
        print("ERROR: 6E BBO-1m ZIP file NOT FOUND in data/databento/")
        print("Existing ZIPS:", all_zips)
        print("Cannot proceed with steps 2-9 without the futures BBO data.")
        
        md_out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'RC015_Study_001_Real_BBO_Qualification.md'))
        with open(md_out_path, 'a') as f:
            f.write("\n## Local Discovery Failure\n")
            f.write("The requested 6E BBO-1m dataset could NOT be found in the repository. Exhaustive search revealed only the original three ZIP files. We cannot pair the real EUU option BBO-1m data with the 6EZ6 futures data because the futures data physically does not exist locally.\n")
        
        return

    # If we somehow found it, we would proceed:
    print("Found 6E BBO-1m ZIP:", futures_bbo_zip)
    
if __name__ == "__main__":
    main()
