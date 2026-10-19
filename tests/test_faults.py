"""Prove startup checks do not treat arbitrary failures as ready labs."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import lab
import native
import sessions


class FaultTests(unittest.TestCase):
    def cli(self,*args):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):code=lab.main(list(args))
        return code,output.getvalue()

    def test_real_blind_git_failure_repair_and_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch.object(native,'ROOT',root),patch.object(sessions,'path',return_value=root/'session.json'),patch.object(lab,'state_path',return_value=root/'attempts.json'):
                self.cli('session','start','013','--blind')
                code,output=self.cli('session','up','--wait','1')
                self.assertEqual(code,0,output)
                self.assertTrue(sessions.current()['fault_verified'])
                self.assertNotIn('CONFLICT',output)
                self.assertNotIn('TIMEOUT',output)
                self.assertEqual(self.cli('session','check')[0],1)
                repo=root/'.lab-state/013/repo'
                (repo/'app.conf').write_text('TIMEOUT=60\nRETRIES=5\n')
                native.git(repo,'add','app.conf');native.git(repo,'commit','-m','Resolve intended settings')
                self.assertEqual(self.cli('session','check')[0],0)
                self.assertEqual(self.cli('session','finish','--score','8')[0],0)
                attempt=lab.attempts()[0]
                self.assertTrue(attempt['startup_verified']);self.assertTrue(attempt['native_verified']);self.assertTrue(attempt['completed'])

    def test_current_recovery_pass_without_a_starting_fault_is_not_completion(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(sessions,'path',return_value=Path(tmp)/'session.json'),patch.object(lab,'state_path',return_value=Path(tmp)/'attempts.json'):
            self.cli('session','start','040')
            with patch.object(native,'operate',return_value=0):
                code,output=self.cli('session','finish','--score','10')
            self.assertEqual(code,2);self.assertIn('no verified starting fault',output)
            self.assertEqual(lab.attempts(),[]);self.assertIsNotNone(sessions.current())

    def test_progressive_hints_and_third_hint_reveal(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(sessions,'path',return_value=Path(tmp)/'session.json'):
            self.cli('session','start','027','--blind')
            self.assertIn('Hint 1/3',self.cli('session','hint')[1])
            self.assertIn('Hint 2/3',self.cli('session','hint')[1])
            self.assertFalse(sessions.current()['revealed'])
            self.assertIn('diagnosis revealed',self.cli('session','hint','--step','3')[1])
            self.assertTrue(sessions.current()['revealed'])

    def test_timeout_does_not_claim_readiness_or_write_proof(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(native,'ROOT',Path(tmp)),patch.object(native,'fault_observed',return_value=False),patch.object(native.time,'monotonic',side_effect=[0,1]):
            output=io.StringIO()
            with contextlib.redirect_stdout(output):code=native.verify_fault('040',wait=1)
            self.assertEqual(code,1);self.assertIn('NOT READY',output.getvalue())
            self.assertFalse((Path(tmp)/'.lab-state/040/startup.json').exists())

    def test_runtime_failure_is_an_error_not_a_confirmed_fault(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(native,'ROOT',Path(tmp)),patch.object(native.shutil,'which',return_value='/bin/git'),patch.object(native,'fault_observed',side_effect=RuntimeError('runtime unavailable')):
            code,output=self.cli('verify-fault','040','--wait','1')
            self.assertEqual(code,2);self.assertIn('runtime unavailable',output)
            self.assertNotIn('READY:',output)

    def test_unrelated_docker_exit_is_not_the_expected_failure(self):
        container={'State':{'Status':'exited','ExitCode':1}}
        with patch.object(native,'docker_info',return_value=container),patch.object(native,'compose',return_value=subprocess.CompletedProcess([],0,'unrelated startup failure','')):
            self.assertFalse(native.fault_observed('019'))
        with patch.object(native,'docker_info',return_value=container),patch.object(native,'compose',return_value=subprocess.CompletedProcess([],0,'required variable APP_MODE missing','')):
            self.assertTrue(native.fault_observed('019'))

    def test_kubernetes_image_failure_requires_client_readiness_and_tag_evidence(self):
        client={'metadata':{'name':'client'},'status':{'conditions':[{'type':'Ready','status':'True'}]}}
        web={'metadata':{'name':'web-abc'},'status':{'containerStatuses':[{'state':{'waiting':{'reason':'ErrImagePull'}}}]}}
        def command(events,ready=True):
            def run(i,*args,**kwargs):
                data={'items':[client,web] if ready else [web]} if args[1]=='pods' else {'items':[{'message':events}]}
                return subprocess.CompletedProcess([],0,json.dumps(data),'')
            return run
        with patch.object(native,'kube',side_effect=command('registry connection timeout')):
            self.assertFalse(native.fault_observed('024'))
        message='Failed to pull busybox:does-not-exist-lab: not found'
        with patch.object(native,'kube',side_effect=command(message,False)):
            self.assertFalse(native.fault_observed('024'))
        with patch.object(native,'kube',side_effect=command(message)):
            self.assertTrue(native.fault_observed('024'))


if __name__=='__main__':unittest.main()
