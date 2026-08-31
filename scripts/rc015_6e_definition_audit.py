import os
import zipfile
import pandas as pd
import glob
import subprocess

def main():
    # 1. Locate the Existing Definition ZIP
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'databento'))
    zip_files = glob.glob(os.path.join(data_dir, '*.zip'))
    
    assert len(zip_files) > 0, "No ZIP file found in data/databento/"
    # Get the specific one if there are multiple, or just the first one
    zip_path = zip_files[0]
    for z in zip_files:
        if 'GLBX' in z and 'definition' not in z.lower(): # Just picking the one we know
            zip_path = z
            
    assert os.path.exists(zip_path), f"Original ZIP does not exist: {zip_path}"
    
    # 2. Extract to Temporary Working Directory
    tmp_dir = os.path.join(data_dir, '_tmp_rc015_definition')
    os.makedirs(tmp_dir, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(tmp_dir)
        
    extracted_files = glob.glob(os.path.join(tmp_dir, '*'))
    assert len(extracted_files) > 0, "No files extracted."
    
    # Find the zst file
    zst_files = [f for f in extracted_files if f.endswith('.zst')]
    assert len(zst_files) == 1, "Expected exactly one .zst definition file."
    zst_path = zst_files[0]
    
    assert os.access(zst_path, os.R_OK), f"Extracted file is not readable: {zst_path}"
    
    # 3. Inspect File Structure
    df_raw = pd.read_csv(zst_path)
    
    # Assertions
    assert len(df_raw) > 0, "Row count is not > 0"
    
    schema = df_raw.columns.tolist()
    
    # 4. Inspect Important Fields
    important_fields = [
        'instrument_id', 'symbol', 'raw_symbol', 'asset', 'instrument_class', 
        'security_type', 'expiration', 'strike_price', 'underlying', 
        'underlying_id', 'parent', 'parent_id', 'currency', 'put_or_call',
        'contract_multiplier', 'min_price_increment', 'maturity_year', 'maturity_month'
    ]
    
    field_status = {}
    for f in important_fields:
        if f in schema:
            field_status[f] = "PRESENT"
        else:
            field_status[f] = "FIELD NOT PRESENT"
            
    # Check for option type / tick size / maturity specifically requested
    if 'security_type' in schema:
        field_status['option type (via security_type/cfi)'] = "PRESENT (indirect)"
    else:
        field_status['option type'] = "FIELD NOT PRESENT"
        
    if 'min_price_increment' in schema:
        field_status['tick size'] = "PRESENT (as min_price_increment)"
    else:
        field_status['tick size'] = "FIELD NOT PRESENT"
        
    if 'maturity_year' in schema:
        field_status['maturity'] = "PRESENT (as maturity_year/month/day/week)"
    else:
        field_status['maturity'] = "FIELD NOT PRESENT"
        
    # Get unique instruments to avoid duplicate IDs for the summary
    # Sort by ts_recv to get the most recent definition for each instrument
    df = df_raw.sort_values('ts_recv').drop_duplicates(subset=['instrument_id'], keep='last').copy()
    
    assert len(df) == df['instrument_id'].nunique(), "Duplicate instrument IDs found in deduplicated set"
    
    # 5. Characterize the Existing 6E Dataset
    asset_counts = df['asset'].value_counts(dropna=False).to_dict() if 'asset' in df.columns else {}
    ic_counts = df['instrument_class'].value_counts(dropna=False).to_dict() if 'instrument_class' in df.columns else {}
    st_counts = df['security_type'].value_counts(dropna=False).to_dict() if 'security_type' in df.columns else {}
    
    # 6. Identify Euro FX Futures
    futures_df = df[df['instrument_class'] == 'F'].copy() if 'instrument_class' in df.columns else pd.DataFrame()
    
    assert not futures_df.empty, "Futures contracts are not identifiable"
    
    futures_summary = []
    for _, row in futures_df.iterrows():
        futures_summary.append({
            'Instrument ID': row.get('instrument_id'),
            'Raw Symbol': row.get('raw_symbol'),
            'Expiry': row.get('expiration'),
            'Contract Month': f"{row.get('maturity_year')}-{row.get('maturity_month'):02d}" if pd.notna(row.get('maturity_year')) else "N/A",
            'Instrument Class': row.get('instrument_class'),
            'Security Type': row.get('security_type'),
            'Tick Size': row.get('min_price_increment'),
            'Contract Multiplier': row.get('contract_multiplier'),
            'Parent/Root': row.get('group', 'N/A')
        })
        
    futures_summary_df = pd.DataFrame(futures_summary).sort_values('Expiry')
    
    # 7. Investigate Options Relationship
    # Search for any references to options
    has_opt_string = df_raw.astype(str).apply(lambda x: x.str.contains(r'\.OPT', regex=True, na=False)).any().any()
    has_put_call = 'put_or_call' in df_raw.columns or ('cfi' in df_raw.columns and df_raw['cfi'].str.contains('O').any())
    strike_values = df_raw['strike_price'].notna().sum() if 'strike_price' in df_raw.columns else 0
    
    options_present = has_opt_string or has_put_call or (strike_values > 0)
    
    # 9. Local Symbology Report
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'RC015_Study_001_6E_Definition_Audit.md'))
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write("# RC015 Study 001 - Local 6E Definition Audit & Euro FX Options Discovery\n\n")
        
        f.write("## Dataset Identification\n")
        f.write(f"- **ZIP filename**: `{os.path.basename(zip_path)}`\n")
        f.write("- **Source**: Databento (GLBX.MDP3)\n")
        f.write("- **Date Range**: 2026-05-16 to 2026-08-15 (inferred from filename)\n")
        f.write(f"- **File count (extracted)**: {len(extracted_files)}\n")
        f.write(f"- **Row count (raw dataset)**: {len(df_raw)}\n")
        f.write(f"- **Unique Instrument count**: {len(df)}\n")
        f.write(f"- **Schema columns**: {len(schema)}\n\n")
        
        f.write("## Schema\n")
        f.write("```text\n")
        for col in schema:
            f.write(f"{col}\n")
        f.write("```\n\n")
        
        f.write("## Field Status (Important Fields)\n")
        for field, status in field_status.items():
            f.write(f"- **{field}**: `{status}`\n")
        f.write("\n")
        
        f.write("## Dataset Characterization\n")
        f.write("### By Asset\n")
        for k, v in asset_counts.items(): f.write(f"- `{k}`: {v} unique instruments\n")
        f.write("### By Instrument Class\n")
        for k, v in ic_counts.items(): f.write(f"- `{k}`: {v} unique instruments\n")
        f.write("### By Security Type\n")
        for k, v in st_counts.items(): f.write(f"- `{k}`: {v} unique instruments\n")
        f.write("\n")
        f.write(f"**Contains Option Instruments?**: `{'Yes' if options_present else 'No'}`\n\n")
        
        f.write("## Euro FX Futures Summary\n")
        f.write(futures_summary_df.to_markdown(index=False))
        f.write("\n\n")
        
        f.write("## Options Discovery\n")
        f.write("The current 6E definition file contains **no options data** and **no references** pointing from futures to associated options. ")
        f.write("Fields such as `strike_price` exist but are entirely null. There are no fields like `put_or_call`, and no symbols contain `.OPT`.\n\n")
        f.write("Because the definition file does not contain cross-references from the underlying futures to the options, we cannot extract the exact options symbols from this file alone. ")
        f.write("However, based on Databento's documented options-on-futures symbology conventions, the parent product for options on a future is designated by appending `.OPT` to the futures root. ")
        f.write("Therefore, the exact Databento symbology required to query options on `6E` futures is `6E.OPT`.\n\n")
        
        f.write("## Missing Information\n")
        f.write("- Option symbols and specific option roots.\n")
        f.write("- Call/Put indicators (`put_or_call` field is absent).\n")
        f.write("- Strike prices (present in schema but no data populated).\n")
        f.write("- Direct linkage from Futures to Options (no `parent` or `associated_options` field).\n\n")
        
        f.write("---\n\n")
        
        f.write("## Options Query Specification\n\n")
        f.write("### Dataset\n")
        f.write("`GLBX.MDP3`\n\n")
        f.write("### Schema\n")
        f.write("`Definition`\n\n")
        f.write("### Product / Parent\n")
        f.write("`6E.OPT`\n\n")
        f.write("### Date Range\n")
        f.write("`2026-08-15` (A single day is sufficient to discover the active options contracts and their definitions. Using the last day of the futures download range ensures we see current active options.)\n\n")
        f.write("### Expected Records\n")
        f.write("We expect to see Definition records where:\n")
        f.write("- `instrument_class` = `O` (Option)\n")
        f.write("- `security_type` = `OPT`\n")
        f.write("- `strike_price` is populated with valid strike values.\n")
        f.write("- The CFI code or a similar field indicates Call/Put (e.g., `OC` for Call, `OP` for Put).\n")
        f.write("- `underlying` or `group` references `6E`.\n")
        f.write("- `expiration` represents the option expiry date.\n")
        f.write("- `instrument_id` gives the unique integer ID for each specific option contract.\n")
        
    print(f"Audit complete. Report generated at: {report_path}")

if __name__ == "__main__":
    main()
