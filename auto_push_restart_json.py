import json
import subprocess
import time
from json import JSONDecodeError


def has_changed(file, last):
    try:
        with open(file, "r", encoding="utf-8") as source:
            current = json.load(source)
    except FileNotFoundError:
        return False, last
    except (OSError, JSONDecodeError) as error:
        print(f"Unable to read {file}: {error}")
        return False, last
    return current != last, current


def publish(file):
    subprocess.run(["git", "add", "--", file], check=True)
    staged_changes = subprocess.run(
        ["git", "diff", "--cached", "--quiet", "--", file],
        check=False,
    )
    if staged_changes.returncode == 1:
        subprocess.run(
            ["git", "commit", "-m", "Auto update restart status", "--", file],
            check=True,
        )
    elif staged_changes.returncode != 0:
        raise subprocess.CalledProcessError(staged_changes.returncode, staged_changes.args)

    subprocess.run(["git", "push"], check=True)


if __name__ == "__main__":
    last_json = {}
    while True:
        changed, new_data = has_changed("restart-time.json", last_json)
        if changed:
            print("Changes detected. Pushing to GitHub...")
            try:
                publish("restart-time.json")
            except subprocess.CalledProcessError as error:
                print(f"Unable to publish restart status (exit {error.returncode}); will retry.")
            except OSError as error:
                print(f"Unable to run Git: {error}; will retry.")
            else:
                last_json = new_data
        time.sleep(60)
