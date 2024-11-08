import pandas as pd
import pickle
import os

# Global file paths
excel_file = "thermo_data.xlsx"     # Main saturation data
shv_file = "shv_table.xlsx"         # Superheated vapor data
cl_file = "cl_table.xlsx"           # Compressed liquid data
ideal_file = "ideal_table.xlsx"     # Ideal gas data (for later)
processed_data_file = "processed_thermo_data.pkl"

def process_excel_data(excel_file, processed_data_file):
    """Process and save the main thermodynamic data."""
    try:
        xls = pd.ExcelFile(excel_file)
        data_dict = {}
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            standardized_sheet_name = sheet_name.lower().replace(' ', '_').replace('-', '_').replace('sat_', '').replace('r134a', 'r_134a')
            data_dict[standardized_sheet_name] = df
        
        with open(processed_data_file, 'wb') as f:
            pickle.dump(data_dict, f)
        print("Data successfully processed and saved.")
        return data_dict
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def load_all_data():
    """Load all thermodynamic data tables."""
    try:
        # Load main saturation data
        with open(processed_data_file, 'rb') as f:
            data_dict = pickle.load(f)
            print("\nSuccessfully loaded saturation data.")
        
        # Load SHV data
        try:
            print("\nAttempting to load SHV table...")
            shv_data = pd.read_excel(shv_file)
            data_dict['water_shv_table'] = shv_data
            print("Successfully loaded superheated vapor table.")
            
        except FileNotFoundError:
            print(f"\nError: Could not find SHV table file: {shv_file}")
            print(f"Please ensure '{shv_file}' is in the same directory as your Python script.")
        except Exception as e:
            print(f"\nError loading SHV table: {e}")
        
        return data_dict
            
    except Exception as e:
        print(f"\nError loading data: {e}")
        return None

def get_user_inputs():
    """Get substance and property inputs from user."""
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

def get_second_property_input(first_property):
    """Get the second property input from user."""
    valid_properties = {
        "pressure": "Press. (bar)",
        "temperature": "Temp. (C)",
        "specific_volume": "Volume (m³/kg)",
        "internal_energy": "Internal Energy (kJ/kg)",
        "enthalpy": "Enthalpy (kJ/kg)",
        "entropy": "Entropy (kJ/kg/K)"
    }
    
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

def determine_table_to_access(substance, property_type):
    """Determine which table to use based on inputs."""
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
    """Find the row containing properties for given temperature or pressure."""
    try:
        # Fix DataFrame structure
        headers = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)
        df.columns = headers
        
        column_mapping = {
            "pressure": "Press. (bar)",
            "temperature": "Temp. (C)"
        }
        
        column_name = column_mapping.get(property_type)
        if not column_name or column_name not in df.columns:
            print(f"Property type '{property_type}' not found in the data.")
            print("Available columns:", df.columns.tolist())
            return None
        
        # Convert columns to numeric
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        property_value = float(property_value)
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
    """Format values with appropriate precision."""
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
            return f"{value}"
    except:
        return str(value)

def calculate_slvm_properties(row, quality):
    """Calculate properties for saturated liquid-vapor mixture."""
    properties = {}
    
    property_pairs = {
        'Volume': ('Volume      (vf, m3/kg)', 'Volume   (vg, m3/kg)'),
        'Internal Energy': ('Internal Energy (uf, kJ/kg)', 'Internal Energy (ug, kJ/kg)'),
        'Enthalpy': ('Enthalpy    (hf, kJ/kg)', 'Enthalpy (hg, kJ/kg)'),
        'Entropy': ('Entropy     (sf, kJ/kg/K)', 'Entropy     (sg, kJ/kg/K)')
    }
    
    for prop_name, (f_col, g_col) in property_pairs.items():
        z_f = float(row[f_col].iloc[0])
        z_g = float(row[g_col].iloc[0])
        z = quality * z_g + (1 - quality) * z_f
        properties[prop_name] = z
    
    return properties

def determine_state_and_properties(row, second_property, second_value, data_dict):
    """
    Determine the state and calculate properties.
    Now includes proper handling of temperature as second property for SHV determination.
    """
    # For temperature as second property, compare with Tsat
    if second_property == "temperature":
        tsat = float(row['Temp. (C)'].iloc[0])
        # Changed column name to match actual data
        pressure = float(row['Press. (bar)'].iloc[0])
        
        if second_value > tsat:
            state = "Superheated Vapor"
            details = f"Temperature ({second_value}°C) is greater than saturation temperature ({tsat}°C)"
            
            # Get SHV table
            df_shv = data_dict.get('water_shv_table')
            if df_shv is not None:
                handle_superheated_vapor(df_shv, second_value, pressure)
            else:
                print("Error: Could not find superheated vapor table.")
            properties = None
            
            return state, details, properties, second_value, pressure
        elif second_value < tsat:
            state = "Compressed Liquid"
            details = f"Temperature ({second_value}°C) is less than saturation temperature ({tsat}°C)"
            properties = None
            print("\nWarning: Compressed liquid state detected. CL table lookup not yet implemented.")
            return state, details, properties, second_value, pressure
        else:
            state = "Saturated"
            details = f"Temperature ({second_value}°C) equals saturation temperature"
            return state, details, None, second_value, pressure
    
    # For other properties, use the existing logic
    property_columns = {
        "specific_volume": ("Volume   (vf, m3/kg)", "Volume   (vg, m3/kg)"),
        "internal_energy": ("Internal Energy    (uf, kJ/kg)", "Internal Energy   (ug, kJ/kg)"),
        "enthalpy": ("Enthalpy    (hf, kJ/kg)", "Enthalpy   (hg, kJ/kg)"),
        "entropy": ("Entropy   (sf, kJ/kg/K)", "Entropy   (sg, kJ/kg/K)")
    }
    
    try:
        if second_property in property_columns:
            f_col, g_col = property_columns[second_property]
            f_value = float(row[f_col].iloc[0])
            g_value = float(row[g_col].iloc[0])
            
            temperature = float(row['Temp. (C)'].iloc[0])
            pressure = float(row['Press. (bar)'].iloc[0])
            
            if second_value < f_value:
                state = "Compressed Liquid"
                details = f"Value ({second_value}) is less than saturated liquid value ({f_value})"
                properties = None
                print("\nWarning: Compressed liquid state detected. CL table lookup not yet implemented.")
                
            elif second_value > g_value:
                state = "Superheated Vapor"
                details = f"Value ({second_value}) is greater than saturated vapor value ({g_value})"
                
                df_shv = data_dict.get('water_shv_table')
                if df_shv is not None:
                    handle_superheated_vapor(df_shv, temperature, pressure)
                else:
                    print("Error: Could not find superheated vapor table.")
                properties = None
                
            elif abs(second_value - f_value) < 1e-6:
                state = "Saturated Liquid"
                details = f"Value ({second_value}) equals saturated liquid value ({f_value})"
                properties = {
                    'Volume': float(row[f_col].iloc[0]),
                    'Internal Energy': float(row['Internal Energy    (uf, kJ/kg)'].iloc[0]),
                    'Enthalpy': float(row['Enthalpy    (hf, kJ/kg)'].iloc[0]),
                    'Entropy': float(row['Entropy   (sf, kJ/kg/K)'].iloc[0])
                }
                
            elif abs(second_value - g_value) < 1e-6:
                state = "Saturated Vapor"
                details = f"Value ({second_value}) equals saturated vapor value ({g_value})"
                properties = {
                    'Volume': float(row[g_col].iloc[0]),
                    'Internal Energy': float(row['Internal Energy   (ug, kJ/kg)'].iloc[0]),
                    'Enthalpy': float(row['Enthalpy   (hg, kJ/kg)'].iloc[0]),
                    'Entropy': float(row['Entropy   (sg, kJ/kg/K)'].iloc[0])
                }
                
            else:
                quality = (second_value - f_value) / (g_value - f_value)
                state = "Saturated Mixture"
                details = f"Value ({second_value}) is between saturated liquid ({f_value}) and vapor ({g_value})\nQuality (x) = {quality:.4f}"
                properties = calculate_slvm_properties(row, quality)
            
            return state, details, properties, temperature, pressure
            
        return "Unknown", "Unable to determine state for this property", None, None, None
            
    except Exception as e:
        print(f"\nError in state determination: {e}")
        # Print the actual column names for debugging
        print("Available columns:", row.columns.tolist())
        return None, None, None, None, None

def find_pressure_bounds(df_shv, target_pressure):
    """
    Find the pressure sections in the SHV table that bound the target pressure.
    """
    current_pressure = None
    current_columns = []
    pressure_sections = []
    
    for col in df_shv.columns:
        if 'p =' in str(col):
            # If we have a previous pressure section, save it
            if current_pressure is not None:
                pressure_sections.append((current_pressure, current_columns))
            
            # Start new pressure section
            pressure_str = str(col)
            pressure_val = float(pressure_str.split('=')[1].split('bar')[0].strip())
            current_pressure = pressure_val
            current_columns = []
        current_columns.append(col)
    
    # Add the last section
    if current_pressure is not None:
        pressure_sections.append((current_pressure, current_columns))
    
    # Find bounding pressures
    for i in range(len(pressure_sections)-1):
        if pressure_sections[i][0] <= target_pressure <= pressure_sections[i+1][0]:
            return pressure_sections[i], pressure_sections[i+1]
    
    return None

def interpolate_value(x, x1, x2, y1, y2):
    """Perform linear interpolation."""
    if x2 - x1 == 0:
        return y1
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

def get_property_value(df_shv, temperature, pressure):
    """
    Get interpolated property values from the SHV table.
    """
    # Find pressure bounds
    pressure_bounds = find_pressure_bounds(df_shv, pressure)
    if not pressure_bounds:
        raise ValueError(f"Pressure {pressure} bar is outside table range")
    
    p1_section, p2_section = pressure_bounds
    p1, p1_cols = p1_section
    p2, p2_cols = p2_section
    
    # Find temperature rows
    temp_column = df_shv['Temp. (C)']
    temp_rows = []
    for i, temp in enumerate(temp_column):
        if isinstance(temp, (int, float)) and not pd.isna(temp):
            if temp >= temperature:
                if i > 0:
                    temp_rows = [i-1, i]
                else:
                    temp_rows = [i, i+1]
                break
    
    if not temp_rows:
        raise ValueError(f"Temperature {temperature}°C is outside table range")
    
    # Get property values at both pressures and temperatures
    properties = {}
    property_names = ['Volume', 'Internal Energy', 'Enthalpy', 'Entropy']
    
    for prop in property_names:
        # Get column names for this property in both pressure sections
        p1_col = [col for col in p1_cols if prop in str(col)][0]
        p2_col = [col for col in p2_cols if prop in str(col)][0]
        
        # Get values at both temperatures for first pressure
        t1_p1 = float(df_shv.iloc[temp_rows[0]][p1_col])
        t2_p1 = float(df_shv.iloc[temp_rows[1]][p1_col])
        
        # Get values at both temperatures for second pressure
        t1_p2 = float(df_shv.iloc[temp_rows[0]][p2_col])
        t2_p2 = float(df_shv.iloc[temp_rows[1]][p2_col])
        
        # Interpolate temperature at each pressure
        temp1 = float(df_shv.iloc[temp_rows[0]]['Temp. (C)'])
        temp2 = float(df_shv.iloc[temp_rows[1]]['Temp. (C)'])
        
        value_p1 = interpolate_value(temperature, temp1, temp2, t1_p1, t2_p1)
        value_p2 = interpolate_value(temperature, temp1, temp2, t1_p2, t2_p2)
        
        # Interpolate between pressures
        final_value = interpolate_value(pressure, p1, p2, value_p1, value_p2)
        properties[prop] = final_value
    
    return properties

def handle_superheated_vapor(df_shv, temperature, pressure):
    """
    Process superheated vapor state and return all properties.
    """
    try:
        properties = get_property_value(df_shv, temperature, pressure)
        
        print("\nSuperheated Vapor Properties:")
        print(f"{'-'*50}")
        print(f"Temperature: {temperature:.3f}°C")
        print(f"Pressure: {pressure:.6f} bar")
        
        for prop, value in properties.items():
            if prop == 'Volume':
                print(f"{prop}: {value:.7f} m³/kg")
            elif prop == 'Entropy':
                print(f"{prop}: {value:.4f} kJ/kg/K")
            else:
                print(f"{prop}: {value:.3f} kJ/kg")
        
        return properties
        
    except Exception as e:
        print(f"\nError in superheated vapor calculations: {e}")
        return None

def main():
    """Main program execution."""
    # Load all data including SHV table
    data_dict = load_all_data()
    
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
                    # Display saturation properties
                    print("\nThermodynamic Properties at Saturation:")
                    print(f"{'-'*50}")
                    
                    # Drop any unnamed columns and format data
                    row = row.loc[:, ~row.columns.str.contains('^Unnamed')]
                    formatted_data = {}
                    for col in row.columns:
                        formatted_data[col] = format_value(row[col].iloc[0], col)
                    
                    # Display formatted saturation data
                    for col, value in formatted_data.items():
                        print(f"{col}: {value}")
                    print(f"{'-'*50}")
                    
                    # Get second property and determine state
                    second_property, second_value = get_second_property_input(first_property)
                    state, details, properties, temperature, pressure = determine_state_and_properties(
                        row, second_property, second_value, data_dict)
                    
                    # Display state and property information
                    if state and details:
                        print(f"\nState Determination:")
                        print(f"{'-'*50}")
                        print(f"State: {state}")
                        print(f"Details: {details}")
                        
                        if properties:
                            print(f"\nCalculated Properties at this State:")
                            print(f"{'-'*50}")
                            for prop, value in properties.items():
                                if 'Volume' in prop:
                                    print(f"{prop}: {value:.7f}")
                                elif 'Entropy' in prop:
                                    print(f"{prop}: {value:.4f}")
                                else:
                                    print(f"{prop}: {value:.3f}")
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