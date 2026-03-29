import pandas as pd

# Define your business data
data = {
    'Product Name': ['Example Item 1', 'Example Item 2'],
    'Selling Price': [100.00, 50.00],
    'Unit Cost (COGS)': [40.00, 15.00],
    'Platform': ['Amazon', 'eBay'],
    'Commission %': [0.15, 0.13], 
    'Fixed Fee': [0.00, 0.30]
}

df = pd.DataFrame(data)
file_name = 'ecommerce_profit_tracker.xlsx'

# Use XlsxWriter to insert live Excel formulas
writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Tracker', index=False)
workbook  = writer.book
worksheet = writer.sheets['Tracker']

# Formats
curr_fmt = workbook.add_format({'num_format': '$#,##0.00'})
perc_fmt = workbook.add_format({'num_format': '0%'})

# Add Formulas to Rows 2 through 100 (pre-filling for future entries)
for row in range(2, 101):
    # Commission $ = (Price * % ) + Fixed Fee
    worksheet.write_formula(f'G{row}', f'=(B{row}*E{row})+F{row}', curr_fmt)
    # Net Profit = Price - Cost - Commission
    worksheet.write_formula(f'H{row}', f'=B{row}-C{row}-G{row}', curr_fmt)
    # Margin % = Profit / Price
    worksheet.write_formula(f'I{row}', f'=IFERROR(H{row}/B{row}, 0)', perc_fmt)

writer.close()
