function displayResults(substance, properties, state)
% displayResults - Displays all thermodynamic properties and state
%
% Inputs:
% substance - String representing the substance name
% properties - Structure containing all properties
% state - String indicating the state (SL, SV, SLVM, SHV, or CL)

% Create a divider line for formatting
divider = repmat('-', 1, 50);

% Display header
fprintf('\n%s\n', divider);
fprintf('Results for %s (State: %s)\n', upper(substance), state);
fprintf('%s\n', divider);

% Display all properties with appropriate units
fprintf('Temperature: %.2f °C\n', properties.temperature);
fprintf('Pressure: %.2f bar\n', properties.pressure);
fprintf('Specific Volume: %.6f m³/kg\n', properties.specific_volume);
fprintf('Internal Energy: %.2f kJ/kg\n', properties.internal_energy);
fprintf('Enthalpy: %.2f kJ/kg\n', properties.enthalpy);
fprintf('Entropy: %.4f kJ/kg·K\n', properties.entropy);

% If state is SLVM, display quality
if strcmp(state, 'SLVM') && isfield(properties, 'quality')
    fprintf('Quality: %.4f\n', properties.quality);
end

fprintf('%s\n\n', divider);
end