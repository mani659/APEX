import os
import pandas as pd
import databento as db

API_KEY = os.environ.get('DATABENTO_API_KEY')
if not API_KEY:
    print("DATABENTO_API_KEY not configured")
    exit(1)
DATASET = 'GLBX.MDP3'

client = db.Historical(API_KEY)

# Test Week: First week of 2024
START_DATE = '2024-01-08T00:00:00'
END_DATE = '2024-01-12T23:59:59'

print(f"Test Period: {START_DATE} to {END_DATE}")

# 1. Product Discovery
print("Discovering symbols...")

# In CME, '6E' is the product code for Euro FX futures.
# Databento symbology: '6E.FUT' and '6E.OPT'
symbols = ['6E.FUT', '6E.OPT']

cost_def = client.metadata.get_cost(
    dataset=DATASET,
    symbols=symbols,
    schema='definition',
    start=START_DATE,
    end=END_DATE,
    stype_in='parent'
)
print(f"Cost to fetch definitions: {cost_def}")

# Let's get the definitions
definitions = client.timeseries.get_range(
    dataset=DATASET,
    symbols=symbols,
    schema='definition',
    start=START_DATE,
    end=END_DATE,
    stype_in='parent'
).to_df()

# Analyze definitions
fut_defs = definitions[definitions['instrument_class'] == 'F']
opt_defs = definitions[definitions['instrument_class'] == 'O']

print(f"Found {len(fut_defs.raw_symbol.unique())} futures contracts.")
print(f"Found {len(opt_defs.raw_symbol.unique())} options contracts.")

# Pick the front-month future (e.g. 6EH4)
active_futures = fut_defs.sort_values('expiration').raw_symbol.unique()
if len(active_futures) > 0:
    front_future = active_futures[0]
    print(f"Selected front-month future: {front_future}")
else:
    print("No futures found")
    exit(1)

# Pick options matching this future expiry or close to it
# We will just pick a subset of options (e.g. ATM, ITM, OTM for the front month) to avoid massive data size
front_opts = opt_defs[opt_defs['raw_symbol'].str.startswith('6EH4')] # This depends on CME nomenclature.
# In CME, Euro FX options have various roots like EW, EUU, 6E, etc. Let's see what raw_symbols we actually get.
print("Sample Option Raw Symbols:")
print(opt_defs['raw_symbol'].unique()[:10])

# Just save the definitions to investigate
definitions.to_csv('definitions_sample.csv')
print("Definitions saved to definitions_sample.csv")

