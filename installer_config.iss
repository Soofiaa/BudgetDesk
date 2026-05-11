; Script de configuración para Inno Setup
; BudgetDesk - Gastos Mensuales

[Setup]
AppId={{7472A582-E7A4-478F-8C92-069E7B362F4A}}
AppName=BudgetDesk
AppVersion=1.0
AppPublisher=BudgetDesk Team
DefaultDirName={autopf}\BudgetDesk
DefaultGroupName=BudgetDesk
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=BudgetDesk_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\BudgetDesk\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\BudgetDesk"; Filename: "{app}\BudgetDesk.exe"
Name: "{commondesktop}\BudgetDesk"; Filename: "{app}\BudgetDesk.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\BudgetDesk.exe"; Description: "{cm:LaunchProgram,BudgetDesk}"; Flags: nowait postinstall skipifsilent