function clTable = getCLTable(substance)
% getCLTable - Returns the compressed liquid data table for the given substance
%
% Inputs:
% substance - String representing the substance name
% 
% Outputs:
% clTable - Table containing compressed liquid properties

% Map substance names to sheet names
sheetMap = struct();
sheetMap.water = 'Compressed Liquid Water';
sheetMap.r134a = 'Compressed Liquid R-134a';
sheetMap.ammonia = 'Compressed Liquid Ammonia';
sheetMap.propane = 'Compressed Liquid Propane';
sheetMap.co2 = 'Compressed Liquid CO2';

% Check if substance is valid and get corresponding sheet name
if ~isfield(sheetMap, substance)
    error('Invalid substance name for compressed liquid table');
end
sheetName = sheetMap.(substance);

% Define the spreadsheet datastore with specific options
opts = spreadsheetImportOptions("NumVariables", 10);
opts.VariableNames = ["Temp", "Col2", "Col3", "Col4", "Col5", "Col6", "Col7", "Col8", "Col9", "Col10"];
opts.VariableTypes = ["string", "string", "string", "string", "string", "string", "string", "string", "string", "string"];

% Read all data as strings to avoid type conversion issues
clTable = readtable("cl_table.xlsx", opts, 'Sheet', sheetName);
end