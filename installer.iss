#define AppName "AI Music Video Studio"
#define AppVersion "0.4.0"
[Setup]
AppId={{E7C9A13F-62CF-4A0A-A929-9173AD3DD0E3}
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={autopf}\AI Music Video Studio
DefaultGroupName={#AppName}
OutputDir=installer-output
OutputBaseFilename=AI-Music-Video-Studio-Setup-0.4.0
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64compatible
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\AI-Music-Video-Studio.exe
[Files]
Source: "dist\AI-Music-Video-Studio\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
[Icons]
Name: "{autoprograms}\AI Music Video Studio"; Filename: "{app}\AI-Music-Video-Studio.exe"
Name: "{autodesktop}\AI Music Video Studio"; Filename: "{app}\AI-Music-Video-Studio.exe"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Crear icono en el escritorio"; GroupDescription: "Accesos directos:"; Flags: checkedonce
[Run]
Filename: "{app}\AI-Music-Video-Studio.exe"; Description: "Abrir AI Music Video Studio"; Flags: nowait postinstall skipifsilent
