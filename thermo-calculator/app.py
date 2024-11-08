from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def determine_state(substance, first_property, first_value, second_property, second_value):
    """
    Determine the thermodynamic state based on the given properties
    """
    # For water at 20°C:
    if substance == 'water' and first_property == 'temperature' and float(first_value) == 20:
        hf = 83.9  # Approximate saturated liquid enthalpy at 20°C
        hg = 2538.1  # Approximate saturated vapor enthalpy at 20°C
        
        if second_property == 'enthalpy':
            h = float(second_value)
            if h < hf:
                return 'Compressed Liquid'
            elif h > hg:
                return 'Superheated Vapor'
            elif abs(h - hf) < 0.1:
                return 'Saturated Liquid'
            elif abs(h - hg) < 0.1:
                return 'Saturated Vapor'
            else:
                quality = (h - hf) / (hg - hf)
                return f'Saturated Liquid-Vapor Mixture (x = {quality:.4f})'

    return 'Saturated'  # Default state if conditions don't match

def get_mock_calculations(substance, first_property, first_value, second_property, second_value):
    """
    Get mock thermodynamic calculations with improved state determination
    """
    state = determine_state(substance, first_property, first_value, second_property, second_value)
    
    # Mock properties based on water at 20°C
    if substance == 'water' and first_property == 'temperature' and float(first_value) == 20:
        hf = 83.9  # Saturated liquid enthalpy
        hg = 2538.1  # Saturated vapor enthalpy
        h = float(second_value) if second_property == 'enthalpy' else 100
        
        if second_property == 'enthalpy':
            quality = (h - hf) / (hg - hf) if hf < h < hg else 0
            details = f"Calculation performed for {substance} at {first_value}°C and {second_value} kJ/kg"
            if 0 < quality < 1:
                details += f" (Quality = {quality:.4f})"
        else:
            details = f"Calculation performed for {substance} at {first_value}°C and {second_value} kJ/kg"

        return {
            'status': 'success',
            'state': state,
            'details': details,
            'saturationProperties': {
                'Temperature (°C)': float(first_value),
                'Pressure (bar)': 0.0234,  # Actual saturation pressure at 20°C
                'Specific Volume (m³/kg)': 1.673,
                'Internal Energy (kJ/kg)': 2506.7,
                'Enthalpy (kJ/kg)': h,
                'Entropy (kJ/kg·K)': 7.3589
            }
        }
    
    # Default mock response for other conditions
    return {
        'status': 'success',
        'state': state,
        'details': f"Calculation performed for {substance} at {first_value} and {second_value}",
        'saturationProperties': {
            'Temperature (°C)': float(first_value) if first_property == 'temperature' else 100.0,
            'Pressure (bar)': float(first_value) if first_property == 'pressure' else 1.013,
            'Specific Volume (m³/kg)': 1.673,
            'Internal Energy (kJ/kg)': 2506.7,
            'Enthalpy (kJ/kg)': float(second_value) if second_property == 'enthalpy' else 2676.1,
            'Entropy (kJ/kg·K)': 7.3589
        }
    }

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        substance = data['substance']
        first_property = data['firstProperty']
        first_value = float(data['firstValue'])
        second_property = data['secondProperty']
        second_value = float(data['secondValue'])

        result = get_mock_calculations(
            substance, 
            first_property, 
            first_value,
            second_property,
            second_value
        )
        
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)