# JVM List Cleaner
Takes CSV files generated from MLS exports and formats the data them to match JVM's Salesforce data standards.


## Requirements
1. You need to run this is the latest version of [Python 3](https://www.python.org/downloads/). It has only been tested on Windows 10. (Make sure to add it to your PATH
2. You also need Salesforce CLI, you can download it here for your operating system (Windows x64): [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli). After downloading, paste the following into your command prompt: ```pip install -r requirements.txt```
3. (Optional) If you want to automatically update this code, you also need to install [Git](https://git-scm.com/download/win)


## How To Download With Git
1. Launch Command Prompt
2. Paste this command ```git clone https://github.com/tpaduraru/JVMListCleaner.git```
3. You can then open the folder with this command ```start .\JVMListCleaner```


## Creating a Desktop Shortcut

### Manually
1. Right click "Start JVM List Cleaner.bat" and create a shortcut.
2. Right click the shortcut, select properties.
3. Go to Shortcut > Change Icon > OK > Browse > JVMListCleaner folder > res > icon.ico, then confirm all the menus
4. Now you can copy the shortcut to your Desktop.

### With PowerShell
1. Sift + Right Click in the JVMListCleaner Directory
2. Select "Open PowerShell Window Here
3. Copy and Paste the following PowerShell script
```
$DesktopPath = Join-Path $Env:OneDriveCommercial "Desktop"
$CurrentPath = $PWD.Path
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\JVM List Cleaner.lnk")
$Shortcut.TargetPath = "$CurrentPath\Start JVM List Cleaner.bat"
$Shortcut.WorkingDirectory = "$CurrentPath"
$Shortcut.IconLocation = "$CurrentPath\res\icon.ico"
$Shortcut.Save()

```


## How To Use
1. Select the file you want to format.
2. Hit the map button, the program will do its best to map all the fields.
3. Edit the map dropdown where necessary.
4. Hit Verify.


## How To Update
Run this command in the JVMListCleaner directory
```
git pull origin main
```
