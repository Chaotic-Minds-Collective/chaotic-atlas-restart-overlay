import contextlib
import io
import json
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("auto_push_restart_json.py")


class StopPolling(Exception):
    pass


class PublisherTests(unittest.TestCase):
    def test_unreadable_input_retains_last_value(self):
        """Bad saves retain the previous value and allow later valid reads."""
        functions = runpy.run_path(str(SCRIPT))
        last = {"seconds_left": 10}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "restart-time.json"
            for content in (b'\xff', b'{"seconds_left":'):
                with self.subTest(content=content):
                    path.write_bytes(content)
                    with contextlib.redirect_stdout(io.StringIO()):
                        changed, value = functions["has_changed"](path, last)
                    self.assertFalse(changed)
                    self.assertIs(value, last)
            path.unlink()
            self.assertEqual(functions["has_changed"](path, last), (False, last))
            path.write_text('{"seconds_left": 20}', encoding="utf-8")
            self.assertEqual(functions["has_changed"](path, last),
                             (True, {"seconds_left": 20}))

    def test_retry_reverted_input_after_publish_failure(self):
        """Git and OS failures must not suppress publication after a reversion."""
        # A succeeds, B fails, malformed B is skipped, then A must publish again.
        for failure in (subprocess.CalledProcessError(1, ["git", "push"]),
                        OSError("Git unavailable")):
            with self.subTest(failure=type(failure).__name__):
                self.check_polling_retry(failure)

    def check_polling_retry(self, failure):
        """Simulate five polls with one failure and an intervening malformed save."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "restart-time.json"
            values = [b'{"seconds_left": 10}', b'{"seconds_left": 20}',
                      b'{', b'{"seconds_left": 10}', b'{"seconds_left": 10}']
            path.write_bytes(values[0])
            iteration = 0
            pushed = []

            def git_run(command, **kwargs):
                """Record synthetic pushes and fail the second attempt."""
                if command == ["git", "push"]:
                    pushed.append(json.loads(path.read_text(encoding="utf-8")))
                    if len(pushed) == 2:
                        raise failure
                return subprocess.CompletedProcess(command, 0)

            def sleep(seconds):
                """Advance the input fixture and stop after the final poll."""
                nonlocal iteration
                self.assertEqual(seconds, 60)
                iteration += 1
                if iteration == len(values):
                    raise StopPolling
                path.write_bytes(values[iteration])

            real_open = open

            def open_status(file, *args, **kwargs):
                """Redirect only status reads to the temporary fixture."""
                return real_open(path if file == "restart-time.json" else file,
                                 *args, **kwargs)

            with patch("builtins.open", side_effect=open_status), \
                    patch("subprocess.run", side_effect=git_run), \
                    patch("time.sleep", side_effect=sleep), \
                    contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(StopPolling):
                    runpy.run_path(str(SCRIPT), run_name="__main__")
            self.assertEqual(pushed, [{"seconds_left": 10},
                                     {"seconds_left": 20},
                                     {"seconds_left": 10}])

    def test_publish_retries_push_without_another_commit(self):
        """An empty staged diff still pushes previously committed changes."""
        publish = runpy.run_path(str(SCRIPT))["publish"]
        with patch("subprocess.run") as run:
            run.return_value.returncode = 0
            publish("restart-time.json")
        self.assertEqual([call.args[0] for call in run.call_args_list], [
            ["git", "add", "--", "restart-time.json"],
            ["git", "diff", "--cached", "--quiet", "--", "restart-time.json"],
            ["git", "push"],
        ])


if __name__ == "__main__":
    unittest.main()
