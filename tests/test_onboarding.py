import contextlib
import io
import unittest
from unittest.mock import patch
import lab
import onboarding


class OnboardingTests(unittest.TestCase):
    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = lab.main(list(args))
        return result, output.getvalue()

    def test_missing_tool_fails_with_next_step(self):
        with patch.object(onboarding.shutil, 'which', return_value=None):
            code, output = self.run_cli('doctor', '--runtime', 'git')
        self.assertEqual(code, 2)
        self.assertIn('MISSING git', output)
        self.assertIn('Install missing tools', output)

    def test_installed_tools_do_not_claim_runtime_readiness(self):
        with patch.object(onboarding.shutil, 'which', return_value='/bin/tool'):
            code, output = self.run_cli('doctor', '--runtime', 'kubernetes')
        self.assertEqual(code, 0)
        self.assertIn('runtime readiness is not verified', output)
        self.assertIn('docker compose version', output)

    def test_tracks_resolve_to_runnable_cases_without_starting_them(self):
        with patch('native.operate', side_effect=AssertionError('Must not start labs')):
            for name, (_, ids) in onboarding.TRACKS.items():
                code, output = self.run_cli('track', name)
                self.assertEqual(code, 0)
                for ident in ids:
                    self.assertIn(ident, lab.RUNTIMES)
                    self.assertIn(ident, output)
                self.assertIn('No labs have been started', output)

    def test_evidence_mode_needs_no_external_tools(self):
        with patch.object(onboarding.shutil, 'which', side_effect=AssertionError('No tools required')):
            self.assertEqual(self.run_cli('doctor')[0], 0)
