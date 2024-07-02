# Screen Image Capture

## Takes a screenshot of the computer screen when pressing a key.

### Libraries Used
<ul>
<li> pynput</li>
<li> Pillow</li>
</ul>

## Setup

<ul>
<li>python -m venv venv</li>
<li>./venv/Scripts/activate</li>
<li> pip install -r requirements.txt </li>
<li>Change <b>temp_env.py</b> to <b>env.py</b> and configure file env variables to your liking. This is only used for <b>screenshot.py</b>.</li>
</ul>

## Run Script
python screenshot.py

## Run UI
python ui_screenshot.py

## Build Exe

### Create exe directory
<ul>
<li>Create a directory within this repo.</li>
<li>CD into the directory.</li>
</ul>

### CMD executable
`pyinstaller --name Py_Screenshot --onefile ../screenshot.py`

### UI executable
`pyinstaller --name Py_Screenshot --onefile --noconsole ../ui_screenshot.py`

## UI executable save data location
`screenshot_path_save.json`