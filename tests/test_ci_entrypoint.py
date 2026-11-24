"""Test the restricted Molecule entry point without starting containers."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestCiEntrypoint(unittest.TestCase):
    def run_entrypoint(self, *arguments, status=0):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            command = path / "molecule"
            command.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\nexit "$STATUS"\n')
            command.chmod(0o755)
            result = subprocess.run(
                [str(ROOT / "runtests"), *arguments],
                cwd=ROOT,
                env={
                    **os.environ,
                    "HOME": str(path),
                    "PATH": f"{path}:{os.environ['PATH']}",
                    "STATUS": str(status),
                },
                capture_output=True,
                text=True,
            )
        return result

    def test_runs_default_scenario(self):
        result = self.run_entrypoint()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["test"])

    def test_forwards_allowlisted_scenario(self):
        result = self.run_entrypoint("--scenario-name=local")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["test", "--scenario-name=local"])

    def test_rejects_unsupported_arguments(self):
        for argument in ("--driver-name=other", "--all", "--", "-e", "../other"):
            with self.subTest(argument=argument):
                result = self.run_entrypoint(argument)
                self.assertEqual(result.returncode, 2)
                self.assertIn("unsupported", result.stderr.lower())
                self.assertEqual(result.stdout, "")

    def test_returns_molecule_status(self):
        result = self.run_entrypoint(status=17)
        self.assertEqual(result.returncode, 17)

    def test_dangling_user_role_link_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            roles = root / ".ansible" / "roles"
            roles.mkdir(parents=True)
            link = roles / "openwisp.openwisp2"
            link.symlink_to(root / "deleted-checkout")
            fake = root / "molecule"
            fake.write_text(
                "#!/bin/sh\nrole=${ANSIBLE_ROLES_PATH%%:*}\n"
                '[ -L "$role/openwisp.openwisp2" ] || exit 19\n'
            )
            fake.chmod(0o755)
            result = subprocess.run(
                [str(ROOT / "runtests")],
                cwd=ROOT,
                env={
                    **os.environ,
                    "HOME": str(root),
                    "TMPDIR": str(root),
                    "PATH": f"{root}:{os.environ['PATH']}",
                },
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(os.readlink(link), str(root / "deleted-checkout"))
