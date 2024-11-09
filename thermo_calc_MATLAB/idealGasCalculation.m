function idealGasCalculation()
% Function to handle ideal gas calculations
clc
fprintf('=== Ideal Gas Properties Calculator ===\n\n')

% Get substance with correct options and mapping
fprintf('Available substances: Air, CO2, H2O, O2, N2, NH3\n')
substance = upper(input('Enter the substance: ', 's'));

% Map common inputs to sheet names
substanceMap = struct();
substanceMap.WATER = 'H2O';
substanceMap.CO2 = 'CO2';
substanceMap.AMMONIA = 'NH3';
substanceMap.H2O = 'H2O';
substanceMap.AIR = 'Air';
substanceMap.O2 = 'O2';
substanceMap.N2 = 'N2';
substanceMap.NH3 = 'NH3';

% Convert input to correct sheet name
if isfield(substanceMap, substance)
    sheetName = substanceMap.(substance);
else
    error('Invalid substance. Please choose from: Air, CO2, H2O, O2, N2, NH3');
end

% Get temperature in Kelvin
temp_K = input('Enter the temperature (K): ');

% Read ideal gas properties from table
try
    properties = getIdealGasProperties(sheetName, temp_K);
    displayIdealGasResults(sheetName, properties);
catch ME
    fprintf('Error: %s\n', ME.message);
end
end
