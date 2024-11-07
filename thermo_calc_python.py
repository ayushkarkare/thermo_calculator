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
        
       # Standardize sheet names to have uniform format (e.g., water_temp_table)
        standardized_sheet_name = sheet_name.lower().replace(' ', '_').replace('-', '_').replace('sat_', '').replace('r134a', 'r_134a')
        
        # Store the processed DataFrame in a dictionary with standardized sheet names
        data_dict[standardized_sheet_name] = df
    
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
    valid_substances = ["water", "r134a", "ammonia", "co2", "propane"]
    valid_property_types = ["pressure", "temperature"]
    
    while True:
        substance = input("Enter the substance (e.g., Water, R-134a, Ammonia): ").strip().lower().replace(' ', '_').replace('-', '_')
        if substance not in valid_substances:
            print("Invalid substance. Please enter one of the following: Water, R-134a, Ammonia, Propane, or CO2.")
            continue
        break
    
    while True:
        property_type = input("Enter the property type you have (pressure or temperature): ").strip().lower()
        if property_type not in valid_property_types:
            print("Invalid property type. Please enter either 'pressure' or 'temperature'.")
            continue
        break
    
    while True:
        try:
            property_value = float(input(f"Enter the value of {property_type}: "))
            break
        except ValueError:
            print("Invalid value. Please enter a numeric value.")
    
    return substance, property_type, property_value

# Function to determine which table to access based on user inputs
def determine_table_to_access(substance, property_type):
    if property_type == "pressure":
        table_name = f"{substance}_pressure_table"
    elif property_type == "temperature":
        table_name = f"{substance}_temp_table"
    else:
        table_name = None
    return table_name

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
