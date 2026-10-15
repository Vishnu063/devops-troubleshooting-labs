import contextlib,io,json,sys,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import lab,native,sessions

class SessionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
  self.ps=patch.object(sessions,'path',return_value=self.base/'session.json');self.ps.start()
  self.pa=patch.object(lab,'state_path',return_value=self.base/'attempts.json');self.pa.start()
 def tearDown(self):self.ps.stop();self.pa.stop();self.tmp.cleanup()
 def cli(self,*args):
  out=io.StringIO()
  with contextlib.redirect_stdout(out):result=lab.main(list(args))
  return result,out.getvalue()
 def test_hidden_brief_omits_title_cause_and_id(self):
  _,output=self.cli('session','start','027','--hidden')
  c=lab.select('027')
  self.assertIn('Hidden incident',output);self.assertNotIn(c['title'],output);self.assertNotIn(c['cause'],output);self.assertNotIn('027',output)
  self.assertIn('Remaining',output)
 def test_session_cannot_be_silently_overwritten(self):
  self.cli('session','start','001')
  with self.assertRaises(SystemExit):self.cli('session','start','002')
  self.assertEqual(sessions.current()['id'],'001')
 def test_hints_and_reveal_are_recorded(self):
  self.cli('session','start','001');self.cli('session','hint','--step','2');self.cli('session','hint','--step','2')
  self.assertEqual(sessions.current()['hints'],[2])
  self.cli('session','solution');self.cli('session','finish','--score','10')
  row=lab.attempts()[0];self.assertFalse(row['completed']);self.assertTrue(row['solution_revealed'])
 def test_timer_expiry_blocks_qualifying_completion(self):
  self.cli('session','start','001','--minutes','1');s=sessions.current();s['started']-=65;sessions.write(s)
  self.assertIn('TIME EXPIRED',self.cli('session','status')[1])
  self.cli('session','finish','--score','10');self.assertTrue(lab.attempts()[0]['timed_out']);self.assertFalse(lab.attempts()[0]['completed'])
 def test_optional_unlock_requires_three_distinct_completions(self):
  for i in ['001','002','003']:
   self.cli('session','start',i);self.cli('session','finish','--score','8')
  self.assertTrue(sessions.unlocked(2,lab.attempts(),lab.all_cases()))
  self.cli('session','start','035','--unlock','--level','2')
 def test_manual_scores_do_not_unlock(self):
  for i in ['001','002','003']:self.cli('record',i,'--score','10','--minutes','10')
  with self.assertRaises(SystemExit):self.cli('session','start','--unlock','--level','2')
  self.assertIsNone(sessions.current(False))
 def test_native_finish_rechecks_instead_of_trusting_stale_pass(self):
  self.cli('session','start','013');s=sessions.current();s['verified']=True;sessions.write(s)
  with patch.object(native,'operate',return_value=1):self.assertEqual(self.cli('session','finish','--score','9')[0],1)
  self.assertTrue(sessions.current());self.assertEqual(lab.attempts(),[])
 def test_compound_selection_and_timer_validation(self):
  self.cli('session','start','--hidden','--compound')
  self.assertIn(sessions.current()['id'],['M01','M02','M03'])
  self.cli('session','abandon')
  with self.assertRaises(SystemExit):self.cli('session','start','001','--minutes','0')
  self.assertIsNone(sessions.current(False))
 def test_repeated_checks_reject_restarts(self):
  with patch.object(native,'check_docker',return_value=True) as check,patch.object(native,'stability_signature',side_effect=['before','after']):
   self.assertFalse(native.grade('020',samples=3,interval=0));self.assertEqual(check.call_count,3)
 def test_reset_recreates_original_git_fault(self):
  with patch.object(native,'ROOT',self.base):
   self.assertEqual(native.operate('up','040'),0)
   native.git(self.base/'.lab-state/040/repo','revert','--no-edit','HEAD')
   self.assertTrue(native.grade('040'))
   self.assertEqual(native.operate('reset','040'),0);self.assertFalse(native.grade('040'))
   self.assertEqual(native.operate('down','040'),0)
 def test_cluster_guard_rejects_cloud_provider(self):
  payload={'items':[{'metadata':{'name':'devops-labs-control-plane'},'spec':{'providerID':'aws:///zone/i-123'}}]}
  from subprocess import CompletedProcess
  with patch.object(native.shutil,'which',return_value='/bin/kubectl'),patch.object(native,'run',return_value=CompletedProcess([],0,json.dumps(payload),'')):
   with self.assertRaises(RuntimeError):native.guard_cluster()
 def test_cleanup_refuses_unowned_namespace(self):
  from subprocess import CompletedProcess
  payload={'metadata':{'name':'devops-lab-027','labels':{}}}
  with patch.object(native,'kube',return_value=CompletedProcess([],0,json.dumps(payload),'')):
   with self.assertRaises(RuntimeError):native.owned_namespace('027')

if __name__=='__main__':unittest.main()
