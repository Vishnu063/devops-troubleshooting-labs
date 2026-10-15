import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import lab
import native

class PracticeTests(unittest.TestCase):
    def cli(self,*args):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):result=lab.main(list(args))
        return result,output.getvalue()

    def test_catalog_and_filters(self):
        for level,count in [(1,34),(2,33),(3,33)]:
            _,output=self.cli('list','--level',str(level))
            self.assertEqual(len(output.splitlines()),count)
        _,output=self.cli('list','--runnable')
        self.assertEqual(len(output.splitlines()),24)
        _,output=self.cli('list','--tool','kubernetes')
        self.assertIn('023',output);self.assertNotIn('Jenkins',output)

    def test_solutions_are_not_shown_in_brief(self):
        for case in lab.cases():
            _,brief=self.cli('show',case['id'])
            self.assertNotIn(case['cause'],brief)
            _,solution=self.cli('solution',case['id'])
            self.assertIn(case['cause'],solution)

    def test_progress_records_repeated_attempts(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(lab,'state_path',return_value=Path(tmp)/'attempts.json'):
                self.cli('record','23','--score','4','--minutes','25','--hints','3')
                self.cli('record','023','--score','9','--minutes','15')
                _,output=self.cli('progress')
                self.assertIn('1/100 cases attempted',output)
                self.assertIn('2 attempts',output)
                self.assertEqual(len(lab.attempts()),2)

    def test_invalid_id_and_bad_history(self):
        with self.assertRaises(SystemExit):lab.select('101')
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'attempts.json';path.write_text('{broken')
            with patch.object(lab,'state_path',return_value=path):
                with self.assertRaises(SystemExit):lab.attempts()

    def test_evidence_case_has_no_native_action(self):
        self.assertEqual(self.cli('up','100')[0],2)

    def test_git_faults_require_actual_repair(self):
        for i in ['013','040']:
            with self.subTest(case=i),tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/'repo'
                native.init_git(i,path)
                self.assertFalse(native.check_git(i,path))
                if i=='013':
                    (path/'app.conf').write_text('TIMEOUT=60\nRETRIES=5\n')
                    native.git(path,'add','app.conf')
                    self.assertFalse(native.check_git(i,path))
                    native.git(path,'commit','-m','Resolve both intended settings')
                else:native.git(path,'revert','--no-edit','HEAD')
                self.assertTrue(native.check_git(i,path))

    def test_kube_manifest_has_distinct_fault_and_repair(self):
        for i in native.K8S:
            folder=ROOT/'runnable'/i
            broken=json.loads((folder/'broken.json').read_text());fixed=json.loads((folder/'fixed.json').read_text())
            self.assertNotEqual(broken,fixed)
            for obj in broken['items']+fixed['items']:
                self.assertEqual(obj['metadata']['namespace'],'devops-lab-'+i.lower())

if __name__=='__main__':unittest.main()
