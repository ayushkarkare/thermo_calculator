function state = determine_state(table, prop1, val1, prop2, val2)
% determineState - Determines the thermodynamic state given two properties
%
% Inputs:
% table - Table containing saturation data
% prop1 - First property type ('pressure', 'temperature')
% val1  - Value of first property
% prop2 - Second property (can be with spaces: 'specific volume', 'internal energy', etc.)
% val2  - Value of second property
%
% Outputs:
% state - String indicating the state (SL, SV, SLVM, SHV, or CL)

% Clean up prop2 by replacing spaces with underscores
prop2 = strrep(prop2, ' ', '_');

% Map property names to actual column numbers
col_map = struct();
col_map.temperature = 1;    % First column is Temperature
col_map.pressure = 2;       % Second column is Pressure
col_map.specific_volume = [3 7];     % columns for vf and vg
col_map.internal_energy = [4 8];     % columns for uf and ug
col_map.enthalpy = [5 9];           % columns for hf and hg
col_map.entropy = [6 10];           % columns for sf and sg

% Convert table to array for easier handling (skip first row which was headers)
data = table{2:end,:};

% Special case for when prop2 is pressure
if strcmp(prop2, 'pressure')
    % Find saturation pressure at the given temperature
    [~, idx] = min(abs(str2double(data(:,col_map.temperature)) - val1));
    sat_pressure = str2double(data(idx,col_map.pressure));
    
    % Compare val2 (pressure) with saturation pressure
    if val2 == sat_pressure
        state = 'SL/SV';  % At saturation line
    elseif val2 > sat_pressure
        state = 'CL';     % Above saturation pressure = compressed liquid
    else
        state = 'SHV';    % Below saturation pressure = superheated vapor
    end
    return
end

% For all other properties
% Find the row in the data that matches prop1's value
[~, idx] = min(abs(str2double(data(:,col_map.(prop1))) - val1));

% Get the saturation values for prop2 at this condition
sat_liquid = str2double(data(idx,col_map.(prop2)(1))); % _f value
sat_vapor = str2double(data(idx,col_map.(prop2)(2)));  % _g value

% Compare val2 with saturation values to determine state
if val2 == sat_liquid
    state = 'SL';  % Saturated Liquid
elseif val2 == sat_vapor
    state = 'SV';  % Saturated Vapor
elseif val2 > sat_liquid && val2 < sat_vapor
    state = 'SLVM';  % Saturated Liquid-Vapor Mixture
elseif val2 > sat_vapor
    state = 'SHV';  % Superheated Vapor
else  % val2 < sat_liquid
    state = 'CL';   % Compressed Liquid
end

end