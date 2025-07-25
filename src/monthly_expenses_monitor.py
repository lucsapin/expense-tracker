import pandas as pd

# Load CSV with correct column names
df = pd.read_csv('../expenses_working.txt')

# Convert date to datetime and extract month
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# Split by account and save monthly summaries in summary/ folder
for account in ['Personal', 'Shared']:
    account_df = df[df['Account'] == account]
    monthly_summary = account_df.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
    for month in monthly_summary['Month'].unique():
        month_name = pd.to_datetime(month + '-01').strftime('%B_%Y')
        month_df = monthly_summary[monthly_summary['Month'] == month]
        filename = f'{month_name}_summary_{account.lower()}.csv'
        month_df.to_csv(f'../Summary/{filename}', index=False)
        print(f"Monthly summary for {account} ({month_name}) saved in Summary/{filename}")
