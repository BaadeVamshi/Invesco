# # # automate_wacc_mdd.py
# # import pandas as pd
# # from pathlib import Path

# # def compute_mdd_generic(df, date_col, value_col='close', start=None, end=None):
# #     d = df.copy()
# #     d[date_col] = pd.to_datetime(d[date_col])
# #     if start: d = d[d[date_col] >= pd.to_datetime(start)]
# #     if end: d = d[d[date_col] <= pd.to_datetime(end)]
# #     d = d.sort_values(date_col).reset_index(drop=True)
# #     d['peak'] = d[value_col].cummax()
# #     d['drawdown'] = (d[value_col] - d['peak']) / d['peak']
# #     mdd_row = d.loc[d['drawdown'].idxmin()]
# #     mdd = mdd_row['drawdown']
# #     peak_idx = d.loc[:mdd_row.name, value_col].idxmax()
# #     peak_date = d.loc[peak_idx, date_col]
# #     trough_date = mdd_row[date_col]
# #     return {'mdd': float(mdd), 'peak_date': peak_date, 'trough_date': trough_date, 'series': d[[date_col, value_col, 'peak', 'drawdown']]}

# # def annualized_return_generic(df, date_col, value_col='close', start=None, end=None):
# #     d = df.copy()
# #     d[date_col] = pd.to_datetime(d[date_col])
# #     if start: d = d[d[date_col] >= pd.to_datetime(start)]
# #     if end: d = d[d[date_col] <= pd.to_datetime(end)]
# #     d = d.sort_values(date_col)
# #     start_val = d.iloc[0][value_col]
# #     end_val = d.iloc[-1][value_col]
# #     days = (d.iloc[-1][date_col] - d.iloc[0][date_col]).days
# #     years = days / 365.25
# #     if years <= 0:
# #         raise ValueError("Date range must span positive time.")
# #     cagr = (end_val / start_val) ** (1/years) - 1
# #     return {'cagr': float(cagr), 'start_val': start_val, 'end_val': end_val, 'years': years}

# # def automate_all(path, start_date=None, end_date=None, msft_sheet='MSFT_Monthly', spy_sheet='SPY_Monthly', wacc_sheet='MSFT_WACC'):
# #     xls = pd.ExcelFile(path)
# #     msft = pd.read_excel(xls, msft_sheet)
# #     spy = pd.read_excel(xls, spy_sheet)
# #     wacc = pd.read_excel(xls, wacc_sheet)

# #     # Normalize date columns
# #     if 'date' in msft.columns:
# #         msft_date_col = 'date'
# #     elif 'timestamp' in msft.columns:
# #         msft_date_col = 'timestamp'
# #     else:
# #         raise KeyError("MSFT sheet missing 'date' or 'timestamp'")

# #     if 'timestamp' in spy.columns:
# #         spy_date_col = 'timestamp'
# #     elif 'date' in spy.columns:
# #         spy_date_col = 'date'
# #     else:
# #         raise KeyError("SPY sheet missing 'date' or 'timestamp'")

# #     # Compute MDD for MSFT
# #     mdd_res = compute_mdd_generic(msft, msft_date_col, 'close', start=start_date, end=end_date)

# #     # Compute CAGR for SPY & MSFT
# #     spy_cagr = annualized_return_generic(spy, spy_date_col, 'close', start=start_date, end=end_date)
# #     msft_cagr = annualized_return_generic(msft, msft_date_col, 'close', start=start_date, end=end_date)

# #     # Get parameters from WACC sheet if present (Tax Rate etc.)
# #     params = {}
# #     # many spreadsheets put params in unnamed columns; try to extract if present
# #     for col in ['Unnamed: 8','Unnamed: 9']:
# #         if col in wacc.columns:
# #             # nothing here — but we'll attempt to build params map if pairs exist
# #             pass
# #     # Try to read Tax Rate from sheet by searching text match
# #     # (This is conservative: if your param table is in columns Unnamed:8/9 as in the file, we extract it)
# #     if 'Unnamed: 8' in wacc.columns and 'Unnamed: 9' in wacc.columns:
# #         param_df = wacc[['Unnamed: 8','Unnamed: 9']].dropna()
# #         params = dict(zip(param_df['Unnamed: 8'], param_df['Unnamed: 9']))

# #     tax = float(params.get('Tax Rate', 0.30))

# #     # Calculate WACC per row
# #     # Expect wacc sheet to have numeric columns: 'Debt %', 'Equity %', 'Cost of Debt', 'Cost of Equity'
# #     w = wacc.copy()
# #     # Ensure numeric
# #     for col in ['Debt %','Equity %','Cost of Debt','Cost of Equity']:
# #         if col not in w.columns:
# #             raise KeyError(f"Required column '{col}' not found in {wacc_sheet} sheet.")
# #         w[col] = pd.to_numeric(w[col], errors='coerce')

# #     w['WACC_calc'] = w['Equity %'] * w['Cost of Equity'] + w['Debt %'] * w['Cost of Debt'] * (1 - tax)

# #     # Find optimal row (min WACC)
# #     if w['WACC_calc'].isnull().all():
# #         optimal = None
# #     else:
# #         optimal_idx = w['WACC_calc'].idxmin()
# #         optimal = w.loc[optimal_idx, ['Debt %','Equity %','D/E Ratio','Cost of Debt','Relevered Beta','Cost of Equity','WACC_calc']].to_dict()

# #     return {
# #         'mdd': mdd_res,
# #         'spy_cagr': spy_cagr,
# #         'msft_cagr': msft_cagr,
# #         'wacc_table': w[['Debt %','Equity %','D/E Ratio','Cost of Debt','Relevered Beta','Cost of Equity','WACC_calc']],
# #         'optimal': optimal
# #     }

# # if __name__ == "__main__":
# #     # Example usage:
# #     excel_path = Path("MSFT_Monthly - Illustration.xlsx")
# #     start_date = '2019-12-31'
# #     end_date = '2021-12-31'
# #     out = automate_all(excel_path, start_date=start_date, end_date=end_date)
# #     print("MDD:", out['mdd']['mdd'], "peak:", out['mdd']['peak_date'], "trough:", out['mdd']['trough_date'])
# #     print("SPY CAGR:", out['spy_cagr']['cagr'])
# #     print("MSFT CAGR:", out['msft_cagr']['cagr'])
# #     print("Optimal WACC row:", out['optimal'])
# #     # Optionally save WACC table
# #     out['wacc_table'].to_csv("computed_wacc_table.csv", index=False)
# import pandas as pd
# from pathlib import Path

# def compute_mdd_generic(df, date_col, value_col='close', start=None, end=None):
#     d = df.copy()
#     d[date_col] = pd.to_datetime(d[date_col])
#     if start: d = d[d[date_col] >= pd.to_datetime(start)]
#     if end: d = d[d[date_col] <= pd.to_datetime(end)]
#     d = d.sort_values(date_col).reset_index(drop=True)

#     d['peak'] = d[value_col].cummax()
#     d['drawdown'] = (d[value_col] - d['peak']) / d['peak']

#     mdd_row = d.loc[d['drawdown'].idxmin()]
#     mdd = mdd_row['drawdown']

#     peak_idx = d.loc[:mdd_row.name, value_col].idxmax()
#     peak_date = d.loc[peak_idx, date_col]
#     trough_date = mdd_row[date_col]

#     return {
#         'mdd': round(float(mdd) * 100, 2),     # convert to % and round
#         'peak_date': peak_date,
#         'trough_date': trough_date
#     }

# def annualized_return_generic(df, date_col, value_col='close', start=None, end=None):
#     d = df.copy()
#     d[date_col] = pd.to_datetime(d[date_col])
#     if start: d = d[d[date_col] >= pd.to_datetime(start)]
#     if end: d = d[d[date_col] <= pd.to_datetime(end)]
#     d = d.sort_values(date_col)

#     start_val = d.iloc[0][value_col]
#     end_val = d.iloc[-1][value_col]

#     days = (d.iloc[-1][date_col] - d.iloc[0][date_col]).days
#     years = days / 365.25
#     cagr = (end_val / start_val) ** (1/years) - 1

#     return round(float(cagr) * 100, 2)  # return % rounded

# def automate_all(path, start_date=None, end_date=None,
#                  msft_sheet='MSFT_Monthly',
#                  spy_sheet='SPY_Monthly',
#                  wacc_sheet='MSFT_WACC'):

#     xls = pd.ExcelFile(path)
#     msft = pd.read_excel(xls, msft_sheet)
#     spy = pd.read_excel(xls, spy_sheet)
#     wacc = pd.read_excel(xls, wacc_sheet)

#     # Normalize date columns
#     if 'date' in msft.columns:
#         msft_date_col = 'date'
#     else:
#         msft_date_col = 'timestamp'

#     if 'timestamp' in spy.columns:
#         spy_date_col = 'timestamp'
#     else:
#         spy_date_col = 'date'

#     # Compute MDD
#     mdd_res = compute_mdd_generic(msft, msft_date_col, 'close',
#                                   start=start_date, end=end_date)

#     # CAGR
#     spy_cagr = annualized_return_generic(spy, spy_date_col, 'close',
#                                          start=start_date, end=end_date)
#     msft_cagr = annualized_return_generic(msft, msft_date_col, 'close',
#                                           start=start_date, end=end_date)

#     # Extract parameters (Tax Rate)
#     param_df = wacc[['Unnamed: 8', 'Unnamed: 9']].dropna()
#     params = dict(zip(param_df['Unnamed: 8'], param_df['Unnamed: 9']))
#     tax = float(params.get('Tax Rate', 0.30))

#     # WACC Calculation
#     w = wacc.copy()
#     numeric_cols = ['Debt %', 'Equity %', 'Cost of Debt', 'Cost of Equity']
#     for col in numeric_cols:
#         w[col] = pd.to_numeric(w[col], errors='coerce')

#     w['WACC_calc'] = (
#         w['Equity %'] * w['Cost of Equity'] +
#         w['Debt %'] * w['Cost of Debt'] * (1 - tax)
#     )

#     # Round all numeric columns to 2 decimals in %
#     w_rounded = w.copy()
#     for col in ['Debt %','Equity %','Cost of Debt','Relevered Beta','Cost of Equity','WACC_calc']:
#         w_rounded[col] = (w_rounded[col] * 100).round(2)

#     # Optimal WACC
#     optimal_idx = w['WACC_calc'].idxmin()
#     optimal_row = w_rounded.loc[optimal_idx]

#     result = {
#         'MDD %': mdd_res['mdd'],
#         'MDD Peak Date': mdd_res['peak_date'],
#         'MDD Trough Date': mdd_res['trough_date'],
#         'MSFT CAGR %': msft_cagr,
#         'SPY CAGR %': spy_cagr,
#         'WACC Table Rounded': w_rounded,
#         'Optimal WACC Row': optimal_row.to_dict()
#     }

#     return result


# # Example run
# if __name__ == "__main__":
#     path = Path("MSFT_Monthly - Illustration.xlsx")
#     out = automate_all(path, start_date='2019-12-31', end_date='2021-12-31')
#     print(out)
import pandas as pd
from pathlib import Path

def automate_all(path, start_date=None, end_date=None,
                 msft_sheet='MSFT_Monthly',
                 spy_sheet='SPY_Monthly',
                 wacc_sheet='MSFT_WACC'):

    xls = pd.ExcelFile(path)
    wacc = pd.read_excel(xls, wacc_sheet)

    # Extract parameters (Tax Rate)
    param_df = wacc[['Unnamed: 8', 'Unnamed: 9']].dropna()
    params = dict(zip(param_df['Unnamed: 8'], param_df['Unnamed: 9']))
    tax = float(params.get('Tax Rate', 0.30))

    # Convert numeric columns
    w = wacc.copy()
    numeric_cols = ['Debt %', 'Equity %', 'Cost of Debt', 'Cost of Equity']
    for col in numeric_cols:
        w[col] = pd.to_numeric(w[col], errors='coerce')

    # Compute WACC
    w['WACC_calc'] = (
        w['Equity %'] * w['Cost of Equity'] +
        w['Debt %'] * w['Cost of Debt'] * (1 - tax)
    )

    # Find optimal WACC
    optimal_idx = w['WACC_calc'].idxmin()
    optimal_wacc = w.loc[optimal_idx, 'WACC_calc']

    # Convert to % and round
    optimal_wacc_percent = round(float(optimal_wacc) * 100, 2)

    return {
        'Optimal WACC %': optimal_wacc_percent
    }


if __name__ == "__main__":
    start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
    end_date = input("Enter End Date (YYYY-MM-DD): ").strip()

    path = Path("MSFT_Monthly - Illustration.xlsx")

    out = automate_all(path, start_date=start_date, end_date=end_date)
    print(out)
