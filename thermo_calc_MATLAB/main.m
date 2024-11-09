function main()
% Main program with menu for ideal gas or unknown state calculations
clc

while true
    % Display main menu
    fprintf('\n=== Thermodynamic Properties Calculator ===\n')
    fprintf('1. Calculate Unknown State Properties\n')
    fprintf('2. Calculate Ideal Gas Properties\n')
    fprintf('3. Exit Program\n')
    
    % Get user choice
    choice = input('Enter your choice (1-3): ');
    
    switch choice
        case 1
            unknownStateCalculation();
        case 2
            idealGasCalculation();
            % Add prompt to continue
            fprintf('\nPress Enter to return to main menu...');
            input('');
        case 3
            fprintf('Exiting program...\n')
            return
        otherwise
            fprintf('Invalid choice. Please enter 1, 2, or 3.\n')
    end
end
end

function unknownStateCalculation()
% Your existing main function logic for unknown state
[substance, prop1, prop1_value, prop2, prop2_value] = get_user_input();
table = getSubstanceTable(substance, prop1);
state = determine_state(table, prop1, prop1_value, prop2, prop2_value);

switch state
    case 'SL'
        properties = saturatedLookup(table, prop1, prop1_value, state);
        displayResults(substance, properties, state);
    case 'SV'
        properties = saturatedLookup(table, prop1, prop1_value, state);
        displayResults(substance, properties, state);
    case 'SHV'
        fprintf("This substance is in SHV, to calculate the rest of the properties you will need temperature and pressure\n")
        while true
            response = input("Do you want to find properties of the Superheated Vapor? (Y/N): ", 's');
            if strcmpi(response, 'Y')
                clc
                fprintf("Calculating properties for Superheated Vapor state:\n\n")
                temp = input('Enter the temperature (°C): ');
                press = input('Enter the pressure (bar): ');
                properties = calculateSHVCLProperties(substance, state, temp, press);
                displayResults(substance, properties, state);
                break;
            elseif strcmpi(response, 'N')
                return;
            else
                fprintf("Please enter Y or N\n");
            end
        end
    case 'CL'
        fprintf("This substance is in CL, to calculate the rest of the properties you will need temperature and pressure\n")
        while true
            response = input("Do you want to find properties of the Compressed Liquid? (Y/N): ", 's');
            if strcmpi(response, 'Y')
                clc
                fprintf("Calculating properties for Compressed Liquid state:\n\n")
                temp = input('Enter the temperature (°C): ');
                press = input('Enter the pressure (bar): ');
                properties = calculateSHVCLProperties(substance, state, temp, press);
                displayResults(substance, properties, state);
                break;
            elseif strcmpi(response, 'N')
                return;
            else
                fprintf("Please enter Y or N\n");
            end
        end
    otherwise
        properties = mixtureLookup(table, prop1, prop1_value, prop2, prop2_value);
        displayResults(substance, properties, state);
end
end