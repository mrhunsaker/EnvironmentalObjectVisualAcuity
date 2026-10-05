; Inno Setup script.
; Install Inno Setup, then compile this file after running build_windows.bat.
;
; https://jrsoftware.org/isinfo.php

#define MyAppName "Environmental Visual Acuity Calculator"
#define MyAppVersion "2026.10.05"
#define MyAppPublisher "Davis School District"
#define MyAppExeName "VisualAcuityCalculator.exe"

[Setup]
AppId={{A6B7E0F3-6F95-4F77-A6A2-2D77C6A0B7E1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Visual Acuity Calculator
DefaultGroupName={#MyAppName}
OutputDir=installer
OutputBaseFilename=VisualAcuityCalculatorSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\VisualAcuityCalculator.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
