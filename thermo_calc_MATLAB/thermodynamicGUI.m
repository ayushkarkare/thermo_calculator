function thermodynamicGUI()
    % Create and show the main UI window
    fig = uifigure('Name', 'Thermodynamic Properties Calculator');
    fig.Position = [100 100 800 600];

    % Create main menu panel
    mainPanel = uipanel(fig, 'Position', [0 0 800 600]);
    
    % Title
    titleLabel = uilabel(mainPanel);
    titleLabel.Text = 'Thermodynamic Properties Calculator';
    titleLabel.FontSize = 24;
    titleLabel.Position = [200 500 400 40];
    titleLabel.HorizontalAlignment = 'center';

    % Main menu buttons
    unknownStateBtn = uibutton(mainPanel, 'Text', 'Calculate Unknown State Properties');
    unknownStateBtn.Position = [300 350 200 40];
    unknownStateBtn.ButtonPushedFcn = @(btn,event) showUnknownStatePanel();

    idealGasBtn = uibutton(mainPanel, 'Text', 'Calculate Ideal Gas Properties');
    idealGasBtn.Position = [300 280 200 40];
    idealGasBtn.ButtonPushedFcn = @(btn,event) showIdealGasPanel();

    exitBtn = uibutton(mainPanel, 'Text', 'Exit');
    exitBtn.Position = [300 210 200 40];
    exitBtn.ButtonPushedFcn = @(btn,event) delete(fig);

    % Unknown State Panel (initially invisible)
    unknownPanel = uipanel(fig, 'Position', [0 0 800 600], 'Visible', 'off');
    
    % Back button for unknown state panel
    backBtn1 = uibutton(unknownPanel, 'Text', 'Back to Main Menu');
    backBtn1.Position = [20 20 120 40];
    backBtn1.ButtonPushedFcn = @(btn,event) showMainPanel();

    % Substance dropdown for unknown state
    substanceLabel = uilabel(unknownPanel, 'Text', 'Select Substance:');
    substanceLabel.Position = [50 500 100 22];
    
    substanceDropdown = uidropdown(unknownPanel);
    substanceDropdown.Items = {'water', 'r134a', 'ammonia', 'propane', 'co2'};
    substanceDropdown.Position = [160 500 120 22];

    % Property selection dropdowns
    prop1Label = uilabel(unknownPanel, 'Text', 'Property 1:');
    prop1Label.Position = [50 450 100 22];
    
    prop1Dropdown = uidropdown(unknownPanel);
    prop1Dropdown.Items = {'temperature', 'pressure'};
    prop1Dropdown.Position = [160 450 120 22];
    
    value1Label = uilabel(unknownPanel, 'Text', 'Value 1:');
    value1Label.Position = [300 450 60 22];
    
    value1Field = uieditfield(unknownPanel, 'numeric');
    value1Field.Position = [370 450 100 22];

    % Add more controls for Unknown State panel as needed...

    % Ideal Gas Panel (initially invisible)
    idealPanel = uipanel(fig, 'Position', [0 0 800 600], 'Visible', 'off');
    
    % Back button for ideal gas panel
    backBtn2 = uibutton(idealPanel, 'Text', 'Back to Main Menu');
    backBtn2.Position = [20 20 120 40];
    backBtn2.ButtonPushedFcn = @(btn,event) showMainPanel();

    % Add controls for Ideal Gas panel...

    % Panel switching functions
    function showMainPanel()
        mainPanel.Visible = 'on';
        unknownPanel.Visible = 'off';
        idealPanel.Visible = 'off';
    end

    function showUnknownStatePanel()
        mainPanel.Visible = 'off';
        unknownPanel.Visible = 'on';
        idealPanel.Visible = 'off';
    end

    function showIdealGasPanel()
        mainPanel.Visible = 'off';
        unknownPanel.Visible = 'off';
        idealPanel.Visible = 'on';
    end
end