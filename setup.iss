[Setup]
; Базові налаштування
AppName=BusinessFlow
AppVersion=1.0.0
DefaultDirName={autopf}\BusinessFlow
DefaultGroupName=BusinessFlow
OutputDir=.\Output
OutputBaseFilename=BusinessFlow_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin

[Tasks]
; Створення ярлика на робочому столі
Name: "desktopicon"; Description: "Створити ярлик на Робочому столі"; GroupDescription: "Додатково:"; Flags: unchecked

[Files]
; 1. Додаємо головний файл
Source: "C:\Users\yser\Desktop\BusinessFlow\dist\my_app\BusinessFlow.exe"; DestDir: "{app}"; Flags: ignoreversion
; 2. Додаємо всі інші файли бібліотек
Source: "C:\Users\yser\Desktop\BusinessFlow\dist\my_app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "data\*"
[Dirs]
; Створюємо папку data і даємо права на запис, щоб SQLite міг створити там базу
Name: "{app}\data"; Permissions: users-modify

[Icons]
; Налаштування ярликів
Name: "{group}\BusinessFlow"; Filename: "{app}\BusinessFlow.exe"
Name: "{autodesktop}\BusinessFlow"; Filename: "{app}\BusinessFlow.exe"; Tasks: desktopicon

[Run]
; Запуск після встановлення
Filename: "{app}\BusinessFlow.exe"; Description: "Запустити BusinessFlow"; Flags: nowait postinstall skipifsilent
