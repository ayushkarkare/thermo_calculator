function properties = mixtureLookup(table, prop1, val1, prop2, val2)
% mixtureLookup - Returns all properties for saturated liquid-vapor mixture
%
% Inputs:
% table - Table containing saturation data
% prop1 - First property type ('pressure' or 'temperature')
% val1  - Value of first property
% prop2 - Second property for quality calculation
% val2  - Value of second property
%
% Outputs:
% properties - Structure containing all properties including quality

% Map property names to actual column numbers
col_map = struct();
col_map.temperature = 1;
col_map.pressure = 2;
col_map.specific_volume = [3 7];
col_map.internal_energy = [4 8];
col_map.enthalpy = [5 9];
col_map.entropy = [6 10];

% Convert table to array for easier handling
data = table{2:end,:};

% Find the row in the data that matches prop1's value
[~, idx] = min(abs(str2double(data(:,col_map.(prop1))) - val1));

% Get saturation values for the property used to calculate quality
prop2_f = str2double(data(idx,col_map.(prop2)(1))); % sat liquid value
prop2_g = str2double(data(idx,col_map.(prop2)(2))); % sat vapor value

% Calculate quality
quality = (val2 - prop2_f)/(prop2_g - prop2_f);

% Get base properties
properties = struct();
properties.temperature = str2double(data(idx,1));
properties.pressure = str2double(data(idx,2));
properties.quality = quality;

% Calculate all other properties using quality
properties.specific_volume = interpolateProperty(data(idx,:), col_map.specific_volume, quality);
properties.internal_energy = interpolateProperty(data(idx,:), col_map.internal_energy, quality);
properties.enthalpy = interpolateProperty(data(idx,:), col_map.enthalpy, quality);
properties.entropy = interpolateProperty(data(idx,:), col_map.entropy, quality);
end

function val = interpolateProperty(data, columns, quality)
% Helper function to interpolate properties based on quality
f_val = str2double(data(columns(1)));
g_val = str2double(data(columns(2)));
val = f_val + quality * (g_val - f_val);
end