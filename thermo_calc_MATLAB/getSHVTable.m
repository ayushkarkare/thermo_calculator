function shvTable = getSHVTable(substance)
% getSHVTable - Returns the superheated vapor data table for the given substance
%
% Inputs:
% substance - String representing the substance name
%
% Outputs:
% shvTable - Table containing superheated vapor properties

% Map substance names to sheet names
sheetMap = struct();
sheetMap.water = 'Superheated Water Vapor';
sheetMap.r134a = 'Superheated R-134a Vapor';
sheetMap.ammonia = 'Superheated Ammonia Vapor';
sheetMap.propane = 'Superheated Propane Vapor';
sheetMap.co2 = 'Superheated CO2 Vapor';

% Check if substance is valid and get corresponding sheet name
if ~isfield(sheetMap, substance)
    error('Invalid substance name for superheated vapor table');
end
sheetName = sheetMap.(substance);

% Define the spreadsheet datastore with specific options
opts = spreadsheetImportOptions("NumVariables", 10);
opts.VariableNames = ["Temp", "Col2", "Col3", "Col4", "Col5", "Col6", "Col7", "Col8", "Col9", "Col10"];
opts.VariableTypes = ["string", "string", "string", "string", "string", "string", "string", "string", "string", "string"];

% Read all data as strings to avoid type conversion issues
shvTable = readtable("shv_table.xlsx", opts, 'Sheet', sheetName);
end