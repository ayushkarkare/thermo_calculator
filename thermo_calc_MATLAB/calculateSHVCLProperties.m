function properties = calculateSHVCLProperties(substance, state, temp, press)
% calculateSHVCLProperties - Calculates properties for SHV or CL states

% Get appropriate table based on state
if strcmp(state, 'SHV')
    table = getSHVTable(substance);
else  % CL state
    table = getCLTable(substance);
end

% Convert table to cell array
data = table2cell(table);

% Track pressure groups and their property columns
pressures = [];
pressure_cols = [];

% Each pressure group starts with a header containing "p = X bar"
for i = 1:size(data,2)
    if ~isempty(data{2,i}) && contains(string(data{2,i}), 'p = ')
        % Extract pressure value
        press_str = string(data{2,i});
        press_val = str2double(regexp(press_str, '[\d.]+', 'match', 'once'));
        if ~isnan(press_val)
            pressures = [pressures press_val];
            % Store the starting column for v,u,h,s for this pressure
            pressure_cols = [pressure_cols i];
        end
    end
end

% Find the appropriate pressure columns for interpolation
[~, p_idx] = min(abs(pressures - press));

% Get temperature rows
temps = [];
temp_rows = [];
for i = 3:size(data,1)
    if ~isempty(data{i,1}) && ~strcmp(string(data{i,1}), 'Sat.')
        temp_val = str2double(string(data{i,1}));
        if ~isnan(temp_val)
            temps = [temps temp_val];
            temp_rows = [temp_rows i];
        end
    end
end

% Find temperatures for interpolation
[~, t_idx] = min(abs(temps - temp));

% Get actual row indices for interpolation
if temp > temps(t_idx)
    t1_idx = t_idx;
    t2_idx = min(t_idx + 1, length(temps));
else
    t2_idx = t_idx;
    t1_idx = max(t_idx - 1, 1);
end

t1 = temps(t1_idx);
t2 = temps(t2_idx);
row1 = temp_rows(t1_idx);
row2 = temp_rows(t2_idx);

% Get column indices for the properties (v,u,h,s)
col_idx = pressure_cols(p_idx);
prop_cols = [col_idx:col_idx+4];  % Get all property columns

% Initialize properties structure
properties = struct();
properties.temperature = temp;
properties.pressure = press;

% Interpolate each property
% Get properties at t1
v1 = str2double(string(data{row1, prop_cols(1)}));
u1 = str2double(string(data{row1, prop_cols(2)}));
h1 = str2double(string(data{row1, prop_cols(3)}));
s1 = str2double(string(data{row1, prop_cols(4)}));

% Get properties at t2
v2 = str2double(string(data{row2, prop_cols(1)}));
u2 = str2double(string(data{row2, prop_cols(2)}));
h2 = str2double(string(data{row2, prop_cols(3)}));
s2 = str2double(string(data{row2, prop_cols(4)}));

% Perform linear interpolation
if t1 ~= t2
    frac = (temp - t1)/(t2 - t1);
    properties.specific_volume = v1 + frac * (v2 - v1);
    properties.internal_energy = u1 + frac * (u2 - u1);
    properties.enthalpy = h1 + frac * (h2 - h1);
    properties.entropy = s1 + frac * (s2 - s1);
else
    properties.specific_volume = v1;
    properties.internal_energy = u1;
    properties.enthalpy = h1;
    properties.entropy = s1;
end

end