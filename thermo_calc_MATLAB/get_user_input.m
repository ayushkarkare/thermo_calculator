function [substance, prop1, prop1_value, prop2, prop2_value] = get_user_input()
% Collect user input that will eventually be processed

% Define allowed cases
allowed_substances = {'water', 'r134a', 'ammonia', 'propane', 'co2'};
allowed_props = {'temperature', 'pressure', 'specific volume', 'internal energy', 'enthalpy', 'entropy'};

while true
    % Prompt the user to enter the substance
    substance = input('Enter the substance from this list: water, r134a, ammonia, propane, co2: ', 's');

    % Convert the input to lowercase and remove any leading/trailing whitespace
    substance = lower(strtrim(substance));

    % Check if the entered value is in the allowed list
    if ismember(substance, allowed_substances)
        break
    else
        disp('Invalid input. Please enter a valid substance from the list.');
    end
end

% Display the main properties to choose from
disp('Select the first property by entering the corresponding number:');
for i = 1:2
    fprintf('%d: %s\n', i, allowed_props{i});
end

while true
    prop1_idx = input('Enter the number for the first property (1 or 2): ');
    if prop1_idx == 1 || prop1_idx == 2
        prop1 = allowed_props{prop1_idx};
        break
    else
        disp('Invalid input. Please enter either 1 or 2');
    end
end

% Prompt the user for the value of the first property
prop1_value = input(['Enter the value for ' prop1 ': ']);

% Remove the selected property from allowed_props
allowed_props(prop1_idx) = [];

% Display the remaining properties for the user to choose from
disp('Select the second property by entering the corresponding number:');
for i = 1:length(allowed_props)
    fprintf('%d: %s\n', i, allowed_props{i});
end

while true
    prop2_idx = input(['Enter the number for the second property (1 to ' num2str(length(allowed_props)) '): ']);
    if prop2_idx >= 1 && prop2_idx <= length(allowed_props)
        prop2 = allowed_props{prop2_idx};
        break
    else
        disp(['Invalid input. Please enter a number between 1 and ' num2str(length(allowed_props))]);
    end
end

% Prompt the user for the value of the second property
prop2_value = input(['Enter the value for ' prop2 ': ']);

% Display user inputs for verification
disp(['Substance: ' substance]);
disp(['First Property: ' prop1 ', Value: ' num2str(prop1_value)]);
disp(['Second Property: ' prop2 ', Value: ' num2str(prop2_value)]);

end