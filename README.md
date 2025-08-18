# PR Notifier

## Project

This tool is a GitHub Pull Request (PR) notifier. It periodically checks for open PRs using the GitHub API and notifies the user of any new PRs through a Tkinter modal window.

Here's a brief overview of how it works:

- Configuration: The tool loads the API URL and token from the config.json file.
- API Request: It sends a GET request to the GitHub API to fetch open PRs.
- Notification: If there are new PRs that haven't been seen before, it displays a Tkinter modal window with the PR details and a clickable link to open the PR in a web browser.
- Loop: The tool runs in a loop, checking for new PRs every minute.
  You can find the main logic in the main.py file. The configuration is stored in the config.json file.

## Installation

1. **Clone the repository:**

```sh
git clone https://github.com/albertohugo/pr_notifier
cd pr_notifier
```

2. **Install pip dependencies:**

```
pip install -r requirements.txt
```

## Running the Project

To run the project, execute the following command:

```sh
python main.py
```

## Configuration

The config.json file contains the necessary configuration for the project. Here is an example of the config.json file:

```json
{
  "api_url": "https://api.github.com/search/issues?q=is:pr+is:open+repo:albertohugo/pr_notifier+label:to_be_reviewed",
  "pr_url": "https://github.com/albertohugo/pr_notifier/pulls?q=is%3Apr+is%3Aopen+label%3Ato_be_reviewed",
  "token": "yourgithubtokenhere",
  "loop_duration": 60,
  "notify_new_pr": true
}
```

### Configuration Parameters

- **api_url:** The URL of the API endpoint to fetch open PRs.
- **pr_url:** The URL to open when viewing PRs in the browser.
- **token:** Your GitHub authentication token for accessing the API.
- **loop_duration:** Time interval (in seconds) between API checks for new PRs.
- **notify_new_pr:** Enable/disable notifications for new PRs (true/false).

## Generating an Executable with PyInstaller

To generate an executable file using PyInstaller, follow these steps:

1. Install PyInstaller:

```sh
pip install pyinstaller
```

2. Generate the executable:

```sh
python -m PyInstaller --onefile --name pr_notifier --add-data resources:resources --add-data config.json:config.json --noconsole main.py
```

This will create a dist folder containing the main.exe file.

## Copying config.json to the Executable Folder

To ensure that config.json is available to the executable, copy it to the same folder as main.exe:

1. Copy config.json to the dist folder:

`cp config.json dist/`

Now, you can run the executable from the dist folder:

```sh
cd dist
./main.exe
```

## Configure the exe as Windows startup

To add main.exe to Windows startup, you can create a shortcut to the executable and place it in the Startup folder. Here are the steps:

1. Press Win + R to open the Run dialog.
2. Type shell:startup and press Enter. This will open the Startup folder.
3. Create a shortcut to main.exe and place it in the Startup folder.

Alternatively, you can use a script to automate this process. Here is a PowerShell script that creates a shortcut to main.exe in the Startup folder:

```powershell
$shortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\main.lnk"
$targetPath = "<PATH>\pr-notifier\main.exe"

$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.Save()
```

Save this script as add_to_startup.ps1 and run it using PowerShell:

`powershell -ExecutionPolicy Bypass -File add_to_startup.ps1`

This will create a shortcut to main.exe in the Startup folder, ensuring it runs at Windows startup.
