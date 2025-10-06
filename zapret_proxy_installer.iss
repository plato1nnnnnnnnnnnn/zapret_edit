; Скрипт для Inno Setup
[Setup]
AppName=Zapret Proxy
AppVersion=1.0
DefaultDirName={pf}\ZapretProxy
DefaultGroupName=Zapret Proxy
OutputDir=dist
OutputBaseFilename=ZapretProxySetup
SetupIconFile=icon.ico

[Files]
Source: "dist\zapret_proxy.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Запрет Proxy"; Filename: "{app}\zapret_proxy.exe"; IconFilename: "{app}\icon.ico"
Name: "{userstartup}\Запрет Proxy"; Filename: "{app}\zapret_proxy.exe"; IconFilename: "{app}\icon.ico"
