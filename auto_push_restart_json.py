import json
import subprocess
import time
from json import JSONDecodeError


def has_changed(file, last):
    """Return (changed, parsed JSON), retaining last on missing or unreadable input."""
    try:
        with open(file, "r", encoding="utf-8") as source:
            current = json.load(source)
    except FileNotFoundError:
        return False, last
    except (OSError, JSONDecodeError, UnicodeDecodeError) as error:
        print(f"Unable to read {file}: {error}")
        return False, last
    return current != last, current


def publish(file):
    """Stage and commit file changes, then push; propagate Git and OS failures.

    Push even without a staged diff so a previously failed push can be retried.
    """
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
    publish_pending = False
    while True:
        # Retry valid input even when it reverts to the last published value.
        comparison_json = object() if publish_pending else last_json
        changed, new_data = has_changed("restart-time.json", comparison_json)
        if changed:
            print("Changes detected. Pushing to GitHub...")
            try:
                publish("restart-time.json")
            except subprocess.CalledProcessError as error:
                publish_pending = True
                print(f"Unable to publish restart status (exit {error.returncode}); will retry.")
            except OSError as error:
                publish_pending = True
                print(f"Unable to run Git: {error}; will retry.")
            else:
                last_json = new_data
                publish_pending = False
        time.sleep(60)
