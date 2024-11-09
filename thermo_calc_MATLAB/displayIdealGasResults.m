function displayIdealGasResults(substance, properties)
% Function to display ideal gas results
divider = repmat('-', 1, 50);

fprintf('\n%s\n', divider);
fprintf('Ideal Gas Properties for %s\n', substance);
fprintf('%s\n', divider);
fprintf('Temperature: %.2f K\n', properties.temperature);
fprintf('Enthalpy: %.4f kJ/kg\n', properties.enthalpy);
fprintf('Internal Energy: %.4f kJ/kg\n', properties.internal_energy);
fprintf('Entropy: %.4f kJ/kg·K\n', properties.entropy);
fprintf('%s\n\n', divider);
end