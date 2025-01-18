import pyreadstat
import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

# Define input and output paths
number_of_columns = 1000
number_of_rows = 20  # Change this to the desired number of rows


sav_filename = "sav_wave4.sav"

data_folder = "data"
output_folder = "build"
excel_filename = sav_filename.replace(".sav", ".xlsx")
input_spss_filename = f"{data_folder}/{sav_filename}"
output_path_excel = f"{output_folder}/{excel_filename}"
#df_data.to_pickle("df_loctimedrink.pkl")

# Read the SPSS (.sav) file
df_data, meta = pyreadstat.read_sav(input_spss_filename)

# Print information about the loaded file
print(
    f"Onze SPSS (.sav) file {input_spss_filename} werd ingelezen en heeft {meta.number_columns} kolommen en {meta.number_rows} rijen."
)

# Select the first 1000 columns if they exist
if meta.number_columns > number_of_columns:
    df_data = df_data.iloc[:, :number_of_columns]
    selected_columns = meta.column_names[:number_of_columns]
    selected_labels = [
        label if label is not None else "" for label in meta.column_labels[:number_of_columns]
    ]
else:
    selected_columns = meta.column_names
    selected_labels = [
        label if label is not None else "" for label in meta.column_labels
    ]

# Select the first X rows if they exist
df_limited = df_data.head(number_of_rows)

# Prepare value labels dictionary
value_labels_dict = meta.value_labels  # dict: variable -> {code: label}

# Prepare value labels for metadata DataFrame
value_labels_for_metadata = []
for var in selected_columns:
    if var in value_labels_dict:
        labels = value_labels_dict[var]
        # Format the labels into a string
        labels_str = '; '.join([f"{code}: {label}" for code, label in labels.items()])
    else:
        labels_str = ''
    value_labels_for_metadata.append(labels_str)

# Prepare metadata DataFrame with Value Labels
metadata_df = pd.DataFrame({
    "Column Names": selected_columns,
    "Column Labels": selected_labels,
    "Value Labels": value_labels_for_metadata
})

# Prepare value labels DataFrame for 'Value Labels' sheet
value_labels_list = []
for var, labels in value_labels_dict.items():
    df_labels = pd.DataFrame({
        "Variable": var,
        "Code": list(labels.keys()),
        "Label": list(labels.values())
    })
    value_labels_list.append(df_labels)

if value_labels_list:
    value_labels_df = pd.concat(value_labels_list, ignore_index=True)
else:
    value_labels_df = pd.DataFrame(columns=["Variable", "Code", "Label"])

# Create an Excel writer object and specify the engine
with pd.ExcelWriter(output_path_excel, engine='openpyxl') as writer:
    # Write metadata to a sheet named 'Metadata'
    metadata_df.to_excel(writer, sheet_name='Metadata', index=False)

    # Write value labels to a sheet named 'Value Labels'
    value_labels_df.to_excel(writer, sheet_name='Value Labels', index=False)

    # Write data to a sheet named 'Data'
    df_data.to_excel(writer, sheet_name='Data', index=False)

    # Access the workbook and sheets for formatting
    workbook = writer.book
    metadata_sheet = writer.sheets['Metadata']
    value_labels_sheet = writer.sheets['Value Labels']
    data_sheet = writer.sheets['Data']

    # Apply bold font to headers in all sheets
    for sheet in [metadata_sheet, value_labels_sheet, data_sheet]:
        for cell in sheet["1:1"]:
            cell.font = Font(bold=True)

    # Optionally, adjust column widths
    for sheet in [metadata_sheet, value_labels_sheet, data_sheet]:
        for column_cells in sheet.columns:
            max_length = 0
            column = column_cells[0].column  # Get the column name
            column_letter = get_column_letter(column)
            for cell in column_cells:
                try:
                    cell_length = len(str(cell.value))
                    if cell_length > max_length:
                        max_length = cell_length
                except:
                    pass
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[column_letter].width = adjusted_width