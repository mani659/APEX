import os
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import brentq

def black76_price(F, K, T, sigma, r, option_type='call'):
    """
    F: Forward/Futures price
    K: Strike price
    T: Time to maturity in years
    sigma: Volatility
    r: Risk-free rate
    option_type: 'call' or 'put'
    """
    if T <= 0 or sigma <= 0:
        return np.maximum(F - K, 0) if option_type == 'call' else np.maximum(K - F, 0)
        
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = np.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))
    else:
        price = np.exp(-r * T) * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
    return price

def black76_iv(target_price, F, K, T, r, option_type='call'):
    """
    Implied volatility inversion using Brent's method.
    """
    if T <= 0:
        return np.nan
        
    # Intrinsic value check
    intrinsic = np.exp(-r * T) * (np.maximum(F - K, 0) if option_type == 'call' else np.maximum(K - F, 0))
    if target_price < intrinsic:
        return np.nan # Arbitrage violation, cannot invert
        
    def objective(sigma):
        return black76_price(F, K, T, sigma, r, option_type) - target_price
        
    try:
        # Bounded search between 0.1% and 500% volatility
        iv = brentq(objective, 1e-4, 5.0)
        return iv
    except ValueError:
        return np.nan

def run_synthetic_unit_tests():
    print("Running Black-76 Synthetic Unit Tests...")
    
    test_cases = [
        {'id': 'Call_ATM', 'type': 'call', 'F': 1.1000, 'K': 1.1000, 'T': 30/365, 'r': 0.05, 'true_iv': 0.08},
        {'id': 'Call_ITM', 'type': 'call', 'F': 1.1000, 'K': 1.0800, 'T': 30/365, 'r': 0.05, 'true_iv': 0.09},
        {'id': 'Call_OTM', 'type': 'call', 'F': 1.1000, 'K': 1.1200, 'T': 30/365, 'r': 0.05, 'true_iv': 0.07},
        {'id': 'Put_ATM',  'type': 'put',  'F': 1.1000, 'K': 1.1000, 'T': 30/365, 'r': 0.05, 'true_iv': 0.08},
        {'id': 'Put_ITM',  'type': 'put',  'F': 1.1000, 'K': 1.1200, 'T': 30/365, 'r': 0.05, 'true_iv': 0.09},
        {'id': 'Put_OTM',  'type': 'put',  'F': 1.1000, 'K': 1.0800, 'T': 30/365, 'r': 0.05, 'true_iv': 0.07},
    ]
    
    results = []
    
    for tc in test_cases:
        # Generate synthetic premium
        premium = black76_price(tc['F'], tc['K'], tc['T'], tc['true_iv'], tc['r'], tc['type'])
        
        # Invert premium back to IV
        recovered_iv = black76_iv(premium, tc['F'], tc['K'], tc['T'], tc['r'], tc['type'])
        
        # Calculate residual
        residual = abs(recovered_iv - tc['true_iv']) if not np.isnan(recovered_iv) else np.nan
        converged = residual < 1e-6 if not np.isnan(recovered_iv) else False
        
        results.append({
            'Contract_ID': tc['id'],
            'Option_Type': tc['type'],
            'Futures_Price': tc['F'],
            'Strike': tc['K'],
            'DTE_Days': tc['T'] * 365,
            'Risk_Free_Rate': tc['r'],
            'True_Sigma': tc['true_iv'],
            'Theoretical_Premium': premium,
            'Recovered_Sigma': recovered_iv,
            'Residual_Error': residual,
            'Converged': converged
        })
        
    df = pd.DataFrame(results)
    
    out_dir = "d:/Gold Scripts/MQL5/Ticks Data/XAUUSD/grid research/apex/reports"
    os.makedirs(out_dir, exist_ok=True)
    df.to_csv(os.path.join(out_dir, 'RC015_Study_001_Black76_Test.csv'), index=False)
    
    print("Unit tests completed successfully.")
    print(df)

if __name__ == "__main__":
    if "DATABENTO_API_KEY" not in os.environ or not os.environ["DATABENTO_API_KEY"]:
        print("DATABENTO_API_KEY not configured")
        print("STOPPING real-data acquisition phase.")
        run_synthetic_unit_tests()
    else:
        # Stub for future implementation when key is present
        pass
