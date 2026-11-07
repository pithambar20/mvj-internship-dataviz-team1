from pathlib import Path
import subprocess
import sys


PROJECT_DIR = Path(__file__).resolve().parent
STAGES = [
    ("Collecting and preparing data", Path("Member_1_Data_Preparation\\member1_data_preparation.py")),
    ("Creating visualizations", Path("Member_2_Visualizations\\member2_visualizations.py")),
    ("Building the final story", Path("Member_3_Story_and_Publishing\\member3_story_html.py")),
]


def main():
    for index, (description, relative_script) in enumerate(STAGES, start=1):
        script = PROJECT_DIR / relative_script
        if not script.is_file():
            raise FileNotFoundError(f"Required project script was not found: {script}")

        print(f"[{index}/{len(STAGES)}] {description}...", flush=True)
        result = subprocess.run(
            [sys.executable, script.name],
            cwd=script.parent,
            check=False,
        )
        if result.returncode:
            raise SystemExit(result.returncode)

    output = PROJECT_DIR / "index.html"
    print(f"\nProject complete. Open this file in your browser:\n{output}")


if __name__ == "__main__":
    main()
