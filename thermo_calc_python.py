import pandas as pd
import pickle

# Step 1: Load Excel Data and Process
# Assuming you have an Excel file named 'thermo_data.xlsx' with sheets for each substance
excel_file = "thermo_data.xlsx"
processed_data_file = "processed_thermo_data.pkl"

# Load data from Excel
try:
    xls = pd.ExcelFile(excel_file)
    data_dict = {}
    for sheet_name in xls.sheet_names:
        # Read each sheet into a DataFrame
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Clean and standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace(',', '')
        
        # Store the processed DataFrame in a dictionary
        data_dict[sheet_name.lower().replace(' ', '_').replace('-', '_')] = df
    
    # Save processed data to a pickle file for quick access
    with open(processed_data_file, 'wb') as f:
        pickle.dump(data_dict, f)
    print("Data successfully processed and saved.")
except Exception as e:
    print(f"Error processing data: {e}")

# Load processed data from file
def load_processed_data():
    try:
        with open(processed_data_file, 'rb') as f:
            data_dict = pickle.load(f)
            print(data_dict)
        return data_dict
    except Exception as e:
        print(f"Error loading processed data: {e}")
        return None

# Function to get user inputs
def get_user_inputs():
    substance = input("Enter the substance (e.g., Water, R-134a, Ammonia): ").strip()
    property_type = input("Enter the property type you have (pressure or temperature): ").strip().lower()
    property_value = float(input(f"Enter the value of {property_type}: "))
    print(f"substance: {substance}, property type: {property_type}, property value: {property_value}")
    return substance, property_type, property_value

# Function to determine which table to access based on user inputs
def determine_table_to_access(substance, property_type):
    if property_type == "pressure":
        print(f"table to acces: sat_{substance}_pressure_table")
        return f"sat_{substance}_pressure_table"
    elif property_type == "temperature":
        print(f"table to access: Sat {substance}-Temp Table")
        return f"sat_{substance}_temp_table"
    else:
        print(f"unsure of table to access")
        return None

# Example usage
# Load the preprocessed data
data_dict = load_processed_data()
if data_dict:
    # Get user inputs
    substance, property_type, property_value = get_user_inputs()
    
    # Determine the table to access
    table_name = determine_table_to_access(substance, property_type)
    if table_name and table_name in data_dict:
        df = data_dict[table_name]
        print(f"Accessing data for {substance} from {table_name}")
        print(df.head())
    else:
        print("Invalid substance or property type.")
