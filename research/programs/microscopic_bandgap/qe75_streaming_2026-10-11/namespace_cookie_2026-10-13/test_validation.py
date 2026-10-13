"""Pure mutation checks plus fresh host sockets. No service, MPI or QE launch."""
import copy
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import cookie_owner as c


class Certificate(unittest.TestCase):
    def setUp(self):
        self.job={'unit':'r07-owned-'+'1'*32+'.service','host_cookie':41,'profile_sha256':'a'*64}
        self.fields=dict(MainPID='77',ActiveState='active',InvocationID='2'*32,ControlGroup='/unit')
        for k,v in [('MemoryMax','67108864'),('MemorySwapMax','0'),('TasksMax','4'),('LimitFSIZE','16384'),
                    ('LimitNOFILE','64'),('LimitCORE','0'),('PrivateNetwork','yes'),('PrivateUsers','yes'),
                    ('KillMode','control-group'),('OOMPolicy','kill'),('Delegate','no'),('Restart','no'),('NoNewPrivileges','yes')]:self.fields[k]=v
        self.kernel=dict(memory_max='67108864',swap_max='0',tasks_max='4',oom_group='1')
        st=c.BINARY.stat()
        self.h=dict(event='HELLO',scope='NON_MPI_NAMESPACE_COMPONENT',job=c.digest(self.job),profile='a'*64,
                    pid=77,uid=1001,start_ticks=88,invocation='2'*32,cgroup='/unit',nonce='c'*64,
                    cookies=[42]*3,inherited_sockets=0,interfaces=1,lo_entries=3,up_entries=3,nonlo_entries=0,
                    bad_addresses=0,ns_stat_errno=13,exe_stat_errno=0,exe_dev=st.st_dev,exe_ino=st.st_ino)

    def validate(self,h=None,fields=None,kernel=None):
        with patch.object(c,'proc',return_value={'start_ticks':88}),patch.object(c,'own_cgroup',return_value='/unit'):
            c.validate_observation(h or self.h,self.job,77,fields or self.fields,kernel or self.kernel)

    def test_complete_component_record_with_inode_eacces(self):self.validate()
    def test_missing_or_false_namespace_evidence(self):
        for key,value in [('cookies',[41]*3),('cookies',[42,43,42]),('cookies',[True]*3),('inherited_sockets',1),
                          ('interfaces',2),('interfaces',True),('nonlo_entries',1),('bad_addresses',1),('up_entries',0),('cookies',None)]:
            h={**self.h,key:value}
            with self.assertRaises(c.Refusal):self.validate(h=h)
    def test_live_binding_and_scope_refuse(self):
        for key,value in [('pid',78),('uid',0),('start_ticks',89),('invocation','3'*32),('job','d'*64),
                          ('profile','d'*64),('scope','LOCAL_MPI_COLLECTIVE_ONLY'),('nonce','z'*64),('cgroup','/other')]:
            with self.assertRaises(c.Refusal):self.validate(h={**self.h,key:value})
    def test_manager_kernel_unknown_or_weakened_refuse(self):
        for k in ['PrivateNetwork','PrivateUsers','TasksMax','NoNewPrivileges','KillMode']:
            f={**self.fields,k:'unknown'}
            with self.assertRaises(c.Refusal):self.validate(fields=f)
        for k in self.kernel:
            with self.assertRaises(c.Refusal):self.validate(kernel={**self.kernel,k:'max'})
    def test_executing_image_unknown_refuses(self):
        for key,value in [('exe_stat_errno',13),('exe_ino',0),('exe_dev',0)]:
            with self.assertRaises(c.Refusal):self.validate(h={**self.h,key:value})
    def test_fresh_host_sockets_are_consistent(self):
        cookies=c.fresh_host_cookies();self.assertEqual(len(set(cookies)),1);self.assertGreater(cookies[0],0)
    def test_exact_fixed_command_is_non_mpi(self):
        job={**self.job,'socket':'/private/owner.sock','case':'normal'}
        owner={'pid':3,'start_ticks':4};ls=type('Stat',(),dict(st_dev=1,st_ino=2))()
        cmd=c.launch_command(job,owner,ls)
        self.assertEqual(cmd[cmd.index(str(c.BINARY))],str(c.BINARY))
        for prop in ['PrivateNetwork=yes','PrivateUsers=yes','MemoryMax=67108864','MemorySwapMax=0','TasksMax=4',
                     'LimitNOFILE=64','RuntimeMaxSec=8s']:
            self.assertIn('--property='+prop,cmd)
        self.assertNotIn('mpirun',' '.join(cmd));self.assertNotIn('pw.x',' '.join(cmd))


if __name__=='__main__':
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Certificate))
    result=dict(passed=r.wasSuccessful(),methods=r.testsRun,kind='PURE_CERTIFICATE_MUTATION_AND_FRESH_HOST_SOCKET',MPI_QE_executed=False)
    (c.PRIVATE/'validation_tests.json').write_text(json.dumps(result,indent=2)+'\n')
    sys.exit(0 if r.wasSuccessful() else 1)
