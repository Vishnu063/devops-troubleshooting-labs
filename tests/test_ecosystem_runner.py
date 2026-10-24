from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class EcosystemConsentTests(unittest.TestCase):
    def test_failure_runner_requires_explicit_disposable_policy_before_any_setup(self):
        script = Path(__file__).resolve().parents[1] / 'integrations/ecosystem_lab.py'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'must-not-exist'
            run = subprocess.run([sys.executable, str(script), '--workspace', directory,
                                  '--tools', directory, '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(2, run.returncode)
            self.assertIn('Explicit --allow-disposable-failure is required', run.stderr)
            self.assertFalse(output.exists())
