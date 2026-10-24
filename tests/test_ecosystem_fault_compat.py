"""Regression for an actual Python/Alpine bind-error wording change in CI."""
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import native
class BindFaultCompatibilityTests(unittest.TestCase):
 def test_real_bind_error_wordings_confirm_fault_but_unrelated_exit_does_not(self):
  state={'State':{'Status':'exited','ExitCode':1}}
  with patch.object(native,'docker_info',return_value=state):
   for logs in ('OSError: [Errno 98] Address already in use','OSError: [Errno 98] Address in use'):
    with patch.object(native,'compose',return_value=SimpleNamespace(stdout=logs)):self.assertTrue(native.fault_observed('006'))
   with patch.object(native,'compose',return_value=SimpleNamespace(stdout='Connection refused')):self.assertFalse(native.fault_observed('006'))
  with patch.object(native,'docker_info',return_value={'State':{'Status':'running','ExitCode':0}}):self.assertFalse(native.fault_observed('006'))
