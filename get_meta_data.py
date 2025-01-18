import pandas as pd
import pyreadstat

# Specify the paths
input_path_sav = "data/sav_wave3.sav"
output_path_excel = "metadata_output_wave3.xlsx"

# Read data (not metadata only)
data, meta = pyreadstat.read_sav(input_path_sav)

# Create metadata dictionary
metadata_dict = {
    "Variable Name": meta.column_names,
    "Variable Label": [
        meta.column_names_to_labels.get(var, "") for var in meta.column_names
    ],
}

# Add format information (if available)
if hasattr(meta, 'formats'):
    metadata_dict["Format"] = [
        meta.formats.get(var, "") for var in meta.column_names
    ]

# Add first *non-empty* value for each variable
first_values = []
for var in meta.column_names:
    if var in data.columns:
        non_na_values = data[var].dropna()
        if not non_na_values.empty:
            first_values.append(non_na_values.iloc[0])
        else:
            first_values.append("")
    else:
        first_values.append("")

metadata_dict["First Value"] = first_values

# Add label for the first value, if available
# We look up the variable's value-label dictionary from meta.variable_value_labels
first_value_labels = []
for var, first_val in zip(meta.column_names, first_values):
    if var not in meta.variable_value_labels or first_val == "":
        # Either no label dictionary for this variable or empty first_val
        first_value_labels.append("")
    else:
        # Get the dictionary mapping codes to labels for this variable
        code_label_dict = meta.variable_value_labels[var]

        # Handle the possibility of integer-coded values stored as float
        # Only convert if it's a float and an integer value
        if isinstance(first_val, float) and first_val.is_integer():
            first_val = int(first_val)

        # Look up the label in code_label_dict; default to "" if not found
        first_value_labels.append(code_label_dict.get(first_val, ""))

metadata_dict["Label for First Value"] = first_value_labels

# Build DataFrame and write to Excel
metadata_df = pd.DataFrame(metadata_dict)
metadata_df.to_excel(output_path_excel, index=False)
print(f"Metadata has been written to {output_path_excel}")

# Print all data for the "ID" variable
#print(data["ID"])
