
import pandas as pd

file_path = '/content/sample_data/MSFT_Monthly - Illustration.xlsx'

# Get all sheet names
xls = pd.ExcelFile(file_path)
print("Sheets in file:", xls.sheet_names)

import pandas as pd

# 1️⃣ Paths to your Excel files
msft_file = '/content/sample_data/MSFT_Monthly.xlsx'  # update with your actual path
sp_file = '/content/sample_data/SandpIndex.xlsx'    # update with your actual path

# 2️⃣ Read Excel files
msft_df = pd.read_excel(msft_file)
sp_df = pd.read_excel(sp_file)

# 3️⃣ Strip column names to avoid issues with spaces
msft_df.columns = msft_df.columns.str.strip()
sp_df.columns = sp_df.columns.str.strip()

# 4️⃣ Function to calculate MDD from Drawdown column
def calculate_mdd(df, drawdown_column='Drawdown'):
    # Convert to numeric in case values are stored as strings
    drawdowns = pd.to_numeric(df[drawdown_column], errors='coerce')
    return drawdowns.min()  # Maximum Drawdown (most negative value)

# 5️⃣ Calculate MDD for both
msft_mdd = calculate_mdd(msft_df)
sp_mdd = calculate_mdd(sp_df)

# 6️⃣ Print results
print("📊 Maximum Drawdown (MDD) Results:")
print(f"MSFT MDD: {abs(msft_mdd*100):.2f}%")
print(f"S&P 500 MDD: {abs(sp_mdd*100):.2f}%")


# 7️⃣ Compare risk
if abs(msft_mdd) < abs(sp_mdd):
    print("✅ MSFT is less risky than S&P 500 based on MDD.")
elif abs(msft_mdd) > abs(sp_mdd):
    print("✅ S&P 500 is less risky than MSFT based on MDD.")
else:
    print("⚠️ MSFT and S&P 500 have the same MDD risk.")

import pandas as pd
import matplotlib.pyplot as plt

# 1️⃣ Paths to your Excel files
msft_file = '/content/sample_data/MSFT_Monthly.xlsx'
sp_file = '/content/sample_data/SandpIndex.xlsx'

# 2️⃣ Read Excel files
msft_df = pd.read_excel(msft_file)
sp_df = pd.read_excel(sp_file)

# 3️⃣ Strip column names
msft_df.columns = msft_df.columns.str.strip()
sp_df.columns = sp_df.columns.str.strip()

# 4️⃣ Ensure 'Date' column is datetime
msft_df['Date'] = pd.to_datetime(msft_df['date'])
sp_df['Date'] = pd.to_datetime(sp_df['timestamp'])

# 5️⃣ Function to calculate MDD from Drawdown column
def calculate_mdd(df, drawdown_column='Drawdown'):
    drawdowns = pd.to_numeric(df[drawdown_column], errors='coerce')
    return drawdowns.min()

# 6️⃣ Calculate MDD for reference
msft_mdd = calculate_mdd(msft_df)
sp_mdd = calculate_mdd(sp_df)
print(f"MSFT MDD: {abs(msft_mdd*100):.2f}%")
print(f"S&P 500 MDD: {abs(sp_mdd*100):.2f}%")

# 7️⃣ Plot MSFT Drawdown
plt.figure(figsize=(12,5))
plt.fill_between(msft_df['Date'], msft_df['Drawdown'], 0, color='red')
plt.title('MSFT Monthly Drawdown')
plt.ylabel('Drawdown %')
plt.xlabel('Date')
plt.grid(alpha=0.3)
plt.show()

# 8️⃣ Plot S&P 500 Drawdown
plt.figure(figsize=(12,5))
plt.fill_between(sp_df['Date'], sp_df['Drawdown'], 0, color='blue')
plt.title('S&P 500 Monthly Drawdown')
plt.ylabel('Drawdown %')
plt.xlabel('Date')
plt.grid(alpha=0.3)
plt.show()

# 9️⃣ Compare MSFT vs S&P 500 Drawdown
plt.figure(figsize=(14,6))
plt.plot(msft_df['Date'], msft_df['Drawdown'], color='red', label='MSFT')
plt.plot(sp_df['Date'], sp_df['Drawdown'], color='blue', label='S&P 500')
plt.title('MSFT vs S&P 500 Monthly Drawdown')
plt.ylabel('Drawdown %')
plt.xlabel('Date')
plt.legend()
plt.grid(alpha=0.3)
plt.show()
