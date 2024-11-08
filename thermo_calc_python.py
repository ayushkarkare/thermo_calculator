import pandas as pd
import pickle

# Step 1: Load Excel Data and Process
# Assuming you have an Excel file named 'thermo_data.xlsx' with sheets for each substance
excel_file = "thermo_data.xlsx"
processed_data_file = "processed_thermo_data.pkl"

def process_excel_data(excel_file, processed_data_file):
    try:
        xls = pd.ExcelFile(excel_file)
        data_dict = {}
        for sheet_name in xls.sheet_names:
            # Read each sheet into a DataFrame, skipping no rows
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Standardize sheet names
            standardized_sheet_name = sheet_name.lower().replace(' ', '_').replace('-', '_').replace('sat_', '').replace('r134a', 'r_134a')
            
            # Store the DataFrame in the dictionary
            data_dict[standardized_sheet_name] = df
        
        # Save processed data to a pickle file
        with open(processed_data_file, 'wb') as f:
            pickle.dump(data_dict, f)
        print("Data successfully processed and saved.")
        return data_dict
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

# Main program execution
def main():
    # Load the preprocessed data
    data_dict = load_processed_data()
    
    if data_dict:
        try:
            # Get user inputs
            substance, property_type, property_value = get_user_inputs()
            
            # Determine the table to access
            table_name = determine_table_to_access(substance, property_type)
            
            if table_name and table_name in data_dict:
                df = data_dict[table_name]
                print(f"\n{'='*50}")
                print(f"Thermodynamic Properties for {substance.upper()}")
                print(f"Looking up properties at {property_type}: {property_value}")
                print(f"{'='*50}")
                
                row = get_row_by_property(df, property_type, property_value)
                if row is not None:
                    # Display all properties in a cleaner format
                    print("\nThermodynamic Properties:")
                    print(f"{'-'*50}")
                    # Drop any unnamed columns for cleaner output
                    row = row.loc[:, ~row.columns.str.contains('^Unnamed')]
                    print(row.to_string(index=False))
                    print(f"{'-'*50}")
            else:
                print(f"\nError: Could not find data table for {substance} with {property_type}.")
                print("Please check your inputs and try again.")
                
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again with valid inputs.")
# Load processed data from file
def load_processed_data():
    try:
        with open(processed_data_file, 'rb') as f:
            data_dict = pickle.load(f)
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
        if substance == 'r134a':
                substance = 'r_134a'
                break
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
        print(f"table to access: {table_name}")
    elif property_type == "temperature":
        table_name = f"{substance}_temp_table"
        print(f"table to access: {table_name}")
    else:
        table_name = None
    return table_name

def get_row_by_property(df, property_type, property_value):
    """
    Find and display the row containing all properties for a given temperature or pressure value.
    Maintains exact precision for all values.
    """
    try:
        # First, fix the DataFrame structure by setting proper headers
        headers = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)
        df.columns = headers
        
        # Map property types to their column names
        column_mapping = {
            "pressure": "Press. (bar)",
            "temperature": "Temp. (C)"
        }
        
        column_name = column_mapping.get(property_type)
        if not column_name or column_name not in df.columns:
            print(f"Property type '{property_type}' not found in the data.")
            print("Available columns:", df.columns.tolist())
            return None
        
        # Convert all numeric columns while preserving full precision
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert input value to float for comparison
        property_value = float(property_value)
        
        # Find the exact or closest value
        closest_idx = (df[column_name] - property_value).abs().idxmin()
        matching_row = df.iloc[[closest_idx]]
        
        if matching_row.empty:
            print(f"No data found for {property_type} = {property_value}")
            return None
            
        return matching_row
        
    except Exception as e:
        print(f"Error while processing data: {e}")
        print("DataFrame structure:", df.head())
        return None

def format_value(value, col_name):
    """
    Format values based on their column type
    """
    try:
        if pd.isna(value):
            return ""
        
        if "Press." in col_name:
            return f"{value:.6f}"  # Pressure to 6 decimal places
        elif "Temp." in col_name:
            return f"{value:.3f}"  # Temperature to 3 decimal places
        elif "Volume" in col_name or "vf" in col_name or "vg" in col_name:
            return f"{value:.7f}"  # Volume to 7 decimal places
        elif "Entropy" in col_name or "sf" in col_name or "sg" in col_name:
            return f"{value:.4f}"  # Entropy to 4 decimal places
        elif "Energy" in col_name or "Enthalpy" in col_name:
            return f"{value:.3f}"  # Energy/Enthalpy to 3 decimal places
        else:
            return f"{value}"  # Default format for other values
    except:
        return str(value)

def get_second_property_input(first_property):
    """
    Get the second property from user and its value.
    Excludes the first property from options.
    """
    valid_properties = {
        "pressure": "Press. (bar)",
        "temperature": "Temp. (C)",
        "specific_volume": "Volume (m³/kg)",
        "internal_energy": "Internal Energy (kJ/kg)",
        "enthalpy": "Enthalpy (kJ/kg)",
        "entropy": "Entropy (kJ/kg/K)"
    }
    
    # Remove the first property from options
    del valid_properties[first_property]
    
    while True:
        print("\nAvailable properties to check:")
        for i, (prop, _) in enumerate(valid_properties.items(), 1):
            print(f"{i}. {prop.replace('_', ' ').title()}")
        
        try:
            choice = int(input("\nEnter the number of your chosen property: "))
            if 1 <= choice <= len(valid_properties):
                property_name = list(valid_properties.keys())[choice-1]
                value = float(input(f"Enter the value for {property_name.replace('_', ' ')}: "))
                return property_name, value
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def determine_state(row, second_property, second_value):
    """
    Determine the state of the substance based on the second property value.
    Returns the state and relevant comparison values.
    """
    # Dictionary mapping properties to their saturated liquid and vapor column names
    property_columns = {
        "specific_volume": ("Volume      (vf, m3/kg)", "Volume   (vg, m3/kg)"),
        "internal_energy": ("Internal Energy (uf, kJ/kg)", "Internal Energy (ug, kJ/kg)"),
        "enthalpy": ("Enthalpy    (hf, kJ/kg)", "Enthalpy (hg, kJ/kg)"),
        "entropy": ("Entropy     (sf, kJ/kg/K)", "Entropy     (sg, kJ/kg/K)")
    }
    
    try:
        if second_property in property_columns:
            f_col, g_col = property_columns[second_property]
            f_value = float(row[f_col].iloc[0])
            g_value = float(row[g_col].iloc[0])
            
            # Determine state based on comparison
            if second_value < f_value:
                state = "Compressed Liquid (CL)"
                details = f"Value ({second_value}) is less than saturated liquid value ({f_value})"
            elif second_value > g_value:
                state = "Superheated Vapor (SHV)"
                details = f"Value ({second_value}) is greater than saturated vapor value ({g_value})"
            elif abs(second_value - f_value) < 1e-6:  # Using small tolerance for floating point comparison
                state = "Saturated Liquid (SL)"
                details = f"Value ({second_value}) equals saturated liquid value ({f_value})"
            elif abs(second_value - g_value) < 1e-6:
                state = "Saturated Vapor (SV)"
                details = f"Value ({second_value}) equals saturated vapor value ({g_value})"
            else:
                # Calculate quality for mixture
                quality = (second_value - f_value) / (g_value - f_value)
                state = "Saturated Liquid Vapor Mixture (SLVM)"
                details = f"Value ({second_value}) is between saturated liquid ({f_value}) and vapor ({g_value})\nQuality (x) = {quality:.4f}"
                
            return state, details
        else:
            return "Unknown", "Unable to determine state for this property"
            
    except Exception as e:
        # Print debugging information
        print("\nDebug Information:")
        print("Available columns:", row.columns.tolist())
        print("Looking for columns:", property_columns[second_property])
        raise e


def main():
    # Load the preprocessed data
    data_dict = load_processed_data()
    
    if data_dict:
        try:
            # Get first property inputs
            substance, first_property, first_value = get_user_inputs()
            
            # Determine the table to access
            table_name = determine_table_to_access(substance, first_property)
            
            if table_name and table_name in data_dict:
                df = data_dict[table_name]
                print(f"\n{'='*50}")
                print(f"Thermodynamic Properties for {substance.upper()}")
                print(f"Looking up properties at {first_property}: {first_value}")
                print(f"{'='*50}")
                
                row = get_row_by_property(df, first_property, first_value)
                if row is not None:
                    # Display all properties in a cleaner format
                    print("\nThermodynamic Properties at Saturation:")
                    print(f"{'-'*50}")
                    
                    # Drop any unnamed columns
                    row = row.loc[:, ~row.columns.str.contains('^Unnamed')]
                    
                    # Format each value with proper precision
                    formatted_data = {}
                    for col in row.columns:
                        formatted_data[col] = format_value(row[col].iloc[0], col)
                    
                    # Create a formatted string
                    output = []
                    for col, value in formatted_data.items():
                        output.append(f"{col}: {value}")
                    
                    print("\n".join(output))
                    print(f"{'-'*50}")
                    
                    # Get second property and determine state
                    second_property, second_value = get_second_property_input(first_property)
                    state, details = determine_state(row, second_property, second_value)
                    
                    print(f"\nState Determination:")
                    print(f"{'-'*50}")
                    print(f"State: {state}")
                    print(f"Details: {details}")
                    print(f"{'-'*50}")
            else:
                print(f"\nError: Could not find data table for {substance} with {first_property}.")
                print("Please check your inputs and try again.")
                
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again with valid inputs.")

# Run the main program
if __name__ == "__main__":
    main()



