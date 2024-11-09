function substanceTable = getSubstanceTable(substance, prop1)
% getSubstanceTable - Returns the appropriate data table for the given substance and property type.
%
% Syntax: substanceTable = getSubstanceTable(substance, prop1)
%
% Inputs:
% substance - A string representing the substance name (e.g., 'water', 'r134a')
% prop1    - A string specifying the property type ('temperature' or 'pressure')
%
% Outputs:
% substanceTable - A table containing thermodynamic properties of the given substance.

% Define the spreadsheet datastore for reading the Excel file
ssds = spreadsheetDatastore('thermo_data.xlsx');

% Define the sheet names mapping to substances and property types
sheetMap = struct();

% Temperature-based tables
sheetMap.temperature = struct();
sheetMap.temperature.water = 'Sat Water-Temp Table';
sheetMap.temperature.r134a = 'R134a-Temp Table';
sheetMap.temperature.ammonia = 'Ammonia-Temp Table';
sheetMap.temperature.propane = 'Propane-Temp Table';
sheetMap.temperature.co2 = 'CO2-Temp Table';

% Pressure-based tables
sheetMap.pressure = struct();
sheetMap.pressure.water = 'Sat Water-Pressure Table';
sheetMap.pressure.r134a = 'R134a-Pressure Table';
sheetMap.pressure.ammonia = 'Ammonia-Pressure Table';
sheetMap.pressure.propane = 'Propane-Pressure Table';
sheetMap.pressure.co2 = 'CO2-Pressure Table';

% Set the appropriate sheet to read
ssds.Sheets = {sheetMap.(prop1).(substance)};

% Read the data from the selected sheet
substanceTable = read(ssds);
end