# Bengaluru Ward Story — 3 Member Project

## Run the whole project

From this folder, install the dependencies and run the project runner:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

The runner executes the three member scripts in order, from their respective folders. Member 1 downloads its source data, so an internet connection is required. When it finishes, open `index.html` in this project folder.

See `TEAM_INSTRUCTIONS.md` for the member role split and details about the data.
