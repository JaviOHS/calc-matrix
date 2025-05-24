[Setup]
AppName=CalcMatrix
AppVersion=1.2
DefaultDirName={pf}\CalcMatrix
DefaultGroupName=CalcMatrix
OutputDir=installer
OutputBaseFilename=CalcMatrixInstaller
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=no
LicenseFile=LICENSE.txt
SetupIconFile=assets\icons\_ico.ico
UninstallDisplayIcon={app}\CalcMatrix v1.2.exe
WizardStyle=modern
AppPublisher=Javier Haro Soledispa
AppPublisherURL=https://github.com/JaviOHS
AppSupportURL=https://github.com/JaviOHS
AppUpdatesURL=https://github.com/JaviOHS/calc-matrix
ShowLanguageDialog=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[CustomMessages]
spanish.WelcomeMsg=Bienvenido al asistente de instalación de CalcMatrix
spanish.WelcomeMsg2=Este asistente te guiará a través del proceso para instalar CalcMatrix v1.2 en tu ordenador.

[Messages]
WelcomeLabel1=Bienvenido al asistente de instalación de CalcMatrix.
WelcomeLabel2=Este asistente te guiará a través del proceso para instalar CalcMatrix v1.2 en tu ordenador.

[Files]
Source: "dist\CalcMatrix v1.2\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CalcMatrix"; Filename: "{app}\CalcMatrix v1.2.exe"
Name: "{commondesktop}\CalcMatrix"; Filename: "{app}\CalcMatrix v1.2.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones adicionales:"

[Run]
Filename: "{app}\CalcMatrix v1.2.exe"; Description: "Ejecutar CalcMatrix"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
