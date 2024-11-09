function properties = getIdealGasProperties(substance, temp_K)
% Function to get ideal gas properties from ideal_table.xlsx

% Read the table as cell array
opts = detectImportOptions('ideal_table.xlsx', 'Sheet', substance);
opts.DataRange = 'A1';
data = readcell('ideal_table.xlsx', 'Sheet', substance);

% Initialize arrays
temps = [];
rows = [];

% Find valid temperature rows (skipping any headers)
for i = 1:size(data,1)
    temp_val = data{i,1};  % Get value from first column
    if ~isempty(temp_val) && isnumeric(temp_val)
        temps = [temps; temp_val];
        rows = [rows; i];
    end
end


% Find closest temperature match
[~, idx] = min(abs(temps - temp_K));

% Get the properties directly for this temperature
row_idx = rows(idx);

% Get properties from the correct columns
properties = struct();
properties.temperature = temp_K;
properties.enthalpy = data{row_idx, 2};         % h [kJ/kg]
properties.internal_energy = data{row_idx, 3};   % u [kJ/kg]
properties.entropy = data{row_idx, 4};          % s° [kJ/kg/K]

% Print final properties for debugging
fprintf('Debug: Final properties:\n');
disp(properties);

end