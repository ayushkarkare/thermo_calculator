function properties = saturatedLookup(table, prop1, val1, state)
% saturatedLookup - Returns all properties for saturated liquid or vapor
%
% Inputs:
% table - Table containing saturation data
% prop1 - Property used for lookup ('pressure' or 'temperature')
% val1  - Value of the lookup property
% state - String indicating state ('SL' or 'SV')
%
% Outputs:
% properties - Structure containing all thermodynamic properties

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

% Find the row in the data that matches prop1's value
[~, idx] = min(abs(str2double(data(:,col_map.(prop1))) - val1));

% Initialize properties structure
properties = struct();
properties.temperature = str2double(data(idx,1));
properties.pressure = str2double(data(idx,2));

% Select column index based on state (first index for SL, second for SV)
suffix_idx = 1 + (strcmp(state, 'SV'));  % 1 for SL, 2 for SV

% Get all properties for the given state
properties.specific_volume = str2double(data(idx,col_map.specific_volume(suffix_idx)));
properties.internal_energy = str2double(data(idx,col_map.internal_energy(suffix_idx)));
properties.enthalpy = str2double(data(idx,col_map.enthalpy(suffix_idx)));
properties.entropy = str2double(data(idx,col_map.entropy(suffix_idx)));

end