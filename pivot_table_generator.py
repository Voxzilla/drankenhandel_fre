import win32com.client as win32

# Open Excel
excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible = True  # Make Excel visible for debugging

# Create a Workbook and Add Data
workbook = excel.Workbooks.Add()
sheet = workbook.Worksheets(1)

# Add sample data
data = [
    ["Category", "SubCategory", "Values"],
    ["A", "X", 10],
    ["B", "Y", 20],
    ["A", "X", 30],
    ["B", "Y", 40],
]

for row_num, row in enumerate(data, start=1):
    for col_num, value in enumerate(row, start=1):
        sheet.Cells(row_num, col_num).Value = value

# Create Pivot Table Cache
source_range = sheet.UsedRange
pivot_cache = workbook.PivotCaches().Create(SourceType=1, SourceData=source_range)

# Add Destination Sheet
pivot_sheet = workbook.Sheets.Add()
pivot_sheet.Name = "Sheet2"

# Create Pivot Table
pivot_table = pivot_cache.CreatePivotTable(
    TableDestination=pivot_sheet.Cells(1, 1),  # Top-left corner of the Pivot Table
    TableName="PivotTable"
)

# Configure Pivot Table
pivot_table.PivotFields("Category").Orientation = 1  # Row
pivot_table.PivotFields("SubCategory").Orientation = 2  # Column
pivot_table.PivotFields("Values").Orientation = 4  # Values

# Save Workbook and Close Excel
workbook.SaveAs("pivot_table_fixed.xlsx")
workbook.Close(False)
excel.Quit()
