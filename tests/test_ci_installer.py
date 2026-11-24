"""Check CI dependency installation and cache placement without network access."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestCiInstaller(unittest.TestCase):
    def test_installs_dependencies_in_review_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            bins = path / "bin"
            bins.mkdir()
            log = path / "calls"
            for name in ("python", "ansible-galaxy"):
                executable = bins / name
                executable.write_text(
                    f'#!/bin/sh\nprintf "%s\\n" "{name} $*" >> "$CALLS"\n'
                )
                executable.chmod(0o755)
            env = {
                **os.environ,
                "HOME": str(path),
                "CI_DEPS_CACHE": str(path / "cache"),
                "PATH": f"{bins}:{os.environ['PATH']}",
                "CALLS": str(log),
            }
            result = subprocess.run(
                [str(ROOT / "install-ci-deps.sh")],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                (path / ".ansible" / "collections").resolve(),
                (path / "cache" / "ansible-collections"),
            )
            self.assertIn(
                "ansible-galaxy collection install --upgrade community.general:>=3.6.0",
                log.read_text(),
            )
            self.assertIn(
                "ansible-galaxy role install --force -r molecule/resources/requirements.yml",
                log.read_text(),
            )
