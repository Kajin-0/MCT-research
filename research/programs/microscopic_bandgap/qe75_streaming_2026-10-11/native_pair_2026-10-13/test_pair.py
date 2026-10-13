"""Focused NEW numerical/phase gates. No MPI, QE main, systemd service or HSE."""
from pathlib import Path
import fcntl
import json
import os
import socket
import struct
import subprocess
import tempfile
import threading
import unittest
import numpy as np

from compare_pair import decode, compare, Refusal, defect, read_regular
from phase_sources import PRIVATE, ROOT
from verify_smoke import verify, HERE, INVOCATION


def packet(path, rank, stage, pad_nan=False, delta=0., changed_input=False, energy=-96.):
    # Independent exact negative Hermitian bath: V=-2 I on 96 physical rows;
    # 48 orthonormal columns span the upper spin component on two ranks.
    # The normalized probe has a lower-spin off-span component:
    # direct and ACE intentionally differ within each member.
    padded, active, bands, spin = 25, 24, 48, 2
    physical = np.r_[np.arange(24), 25+np.arange(24)]
    rows = padded*spin
    layout = np.array([rank, 2, 101, 48], dtype='=i8')
    labels = np.arange(rank*24+1, rank*24+25, dtype='=i8')
    phi = np.zeros((rows, bands), dtype='=c16')
    phi[:24, rank*24:rank*24+24] = np.eye(24)
    if changed_input:
        phi[physical[0], rank*24] *= -1
    probe = np.zeros((rows, 1), dtype='=c16')
    probe[physical, 0] = 1./np.sqrt(96.)
    vphi = -2*phi
    direct = -2*probe
    ace = -2*probe; ace[25:49, :] = 0
    direct[physical[0], 0] += delta
    gram = -2*np.eye(bands, dtype='=c16')
    factor = np.eye(bands, dtype='=c16')/np.sqrt(2.)
    occ = np.ones((48, 1), dtype='=f8')
    xi = np.sqrt(2.)*phi
    if pad_nan:
        phi[[24, 49], :] = complex(float('nan'), 0)
    raw = b'QE75-ACE-DIAG01 '+struct.pack('=9qd', 1, rank, 1, stage,
        padded, active, spin, bands, len(layout), energy)+layout.tobytes()+labels.tobytes()
    if stage == 1:
        raw += struct.pack('=2q', *occ.shape)+occ.tobytes(order='F')
        for j in range(bands):
            raw += phi[:, j].tobytes()+vphi[:, j].tobytes()
        raw += gram.tobytes(order='F')+probe.tobytes(order='F')+direct.tobytes(order='F')
    else:
        raw += xi.tobytes(order='F')+factor.tobytes(order='F')+ace.tobytes(order='F')
    path.write_bytes(raw)
    return path


class PairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = PRIVATE/'focused-tests-final'
        cls.root.mkdir(exist_ok=False)
        fc = ROOT/'toolchain/bin/x86_64-conda-linux-gnu-gfortran'
        obj = cls.root/'model'
        obj.mkdir()
        commands = [
            ['/usr/bin/cc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-O2',
             HERE/'phase_worker.c', PRIVATE/'source/lease_client.c', '-o', cls.root/'wire_worker'],
            [fc, '-O0', '-fcheck=all', '-J', obj, '-c', HERE/'phase_stubs.f90', '-o', obj/'stubs.o'],
            [fc, '-O0', '-fcheck=all', '-J', obj, '-I', obj, '-c', PRIVATE/'source/native_lease.f90', '-o', obj/'lease.o'],
            [fc, '-O0', '-fcheck=all', '-I', obj, HERE/'phase_unit.f90', obj/'lease.o', obj/'stubs.o', '-o', cls.root/'phase_model'],
        ]
        cls.build_records = []
        for c in commands:
            r = subprocess.run(list(map(str, c)), capture_output=True, text=True, timeout=30)
            cls.build_records.append(dict(command=list(map(str, c)), status=r.returncode, stderr=r.stderr))
            if r.returncode:
                raise RuntimeError(r.stderr)
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=self.root)
        self.dir = Path(self.temp.name)
    def tearDown(self):
        self.temp.cleanup()
    def pair(self, **changes):
        a, b = {}, {}
        for r in [0, 1]:
            for s in [1, 2]:
                a[(r, 1, s)] = packet(self.dir/f'a{r}{s}', r, s)
                b[(r, 1, s)] = packet(self.dir/f'b{r}{s}', r, s, **changes)
        return a, b
    def test_corresponding_actions_and_unique_energy_not_direct_equals_ace(self):
        a, b = self.pair()
        result = compare(a, b, [1])
        self.assertTrue(result['passed'])
        self.assertEqual(result['summed_unique_k_energy_delta_Ry'], 0)
        self.assertFalse(np.array_equal(decode(a[(0, 1, 1)])['action'], decode(a[(0, 1, 2)])['action']))
    def test_only_unused_padding_is_excluded_no_phase_repair(self):
        a, b = self.pair(pad_nan=True)
        self.assertTrue(compare(a, b, [1])['passed'])
        for p in b.values():
            p.unlink()
        for r in [0, 1]:
            for s in [1, 2]:
                packet(b[(r, 1, s)], r, s, changed_input=True)
        with self.assertRaisesRegex(Refusal, 'phi'):
            compare(a, b, [1])
        # Unused INPUT padding differs from operator/probe ABI padding, which
        # the native code initializes to zero. Never discard a wrong action.
        p = a[(0, 1, 2)]; raw = bytearray(p.read_bytes())
        struct.pack_into('=d', raw, 96+4*8+24*8+24*16, float('nan')); p.write_bytes(raw)
        with self.assertRaisesRegex(Refusal, 'padding'): decode(p)
    def test_action_energy_coverage_and_live_extent_refusals(self):
        for changes in [dict(delta=1e-8), dict(energy=-96.+1e-8)]:
            with tempfile.TemporaryDirectory(dir=self.root) as d:
                old = self.dir; self.dir = Path(d)
                a, b = self.pair(**changes)
                with self.assertRaises(Refusal): compare(a, b, [1])
                self.dir = old
        a, b = self.pair()
        with self.assertRaises(Refusal): compare(a, {k:v for k,v in b.items() if k!=(1, 1, 2)}, [1])
        p = a[(0, 1, 1)]
        p.write_bytes(p.read_bytes()+b'bad')
        with self.assertRaises(Refusal): decode(p)
        huge = self.dir/'huge'
        with huge.open('wb') as f: f.truncate(129*2**20)
        with self.assertRaises(Refusal): read_regular(huge)
        alias = self.dir/'alias'; alias.symlink_to(p)
        with self.assertRaises(OSError): decode(alias)
        self.assertFalse(defect(np.array([1.]), np.array([1.+2e-12]))['passed'])
    def test_replicated_gram_and_label_corruption_refused(self):
        a, b = self.pair()
        p = b[(1, 1, 1)]; original = p.read_bytes(); raw = bytearray(original)
        gram_offset = 96+4*8+24*8+16+48*8+48*2*50*16
        struct.pack_into('=d', raw, gram_offset, -3.); p.write_bytes(raw)
        with self.assertRaisesRegex(Refusal, 'replicated'): compare(a, b, [1])
        p.write_bytes(original)
        p = b[(1, 1, 1)]; raw = bytearray(p.read_bytes())
        # First reciprocal label becomes a rank-0 label: invalid global cover.
        struct.pack_into('=q', raw, 96+4*8, 1); p.write_bytes(raw)
        with self.assertRaisesRegex(Refusal, 'reciprocal'): compare(a, b, [1])
    def test_equal_but_wrong_ACE_action_is_not_self_validating(self):
        a, b = self.pair()
        # Change the same action entry in BOTH modes. Pairwise equality alone
        # would pass; independent -Xi (sum Xi^dagger probe) must reject it.
        for group in [a, b]:
            for rank in [0, 1]:
                p = group[(rank, 1, 2)]; raw = bytearray(p.read_bytes())
                action = len(raw)-50*16
                v = struct.unpack_from('=d', raw, action)[0]
                struct.pack_into('=d', raw, action, v+1e-6); p.write_bytes(raw)
        with self.assertRaisesRegex(Refusal, 'inconsistency'): compare(a, b, [1])
    def test_new_native_phase_order_and_unchanged_core_source(self):
        init = (PRIVATE/'source/init_run.f90').read_text()
        tail = init.split('SUBROUTINE qe75_capture_initial()', 1)[1]
        self.assertLess(tail.index('ENDDO'), tail.index('CALL native_phase(4)'))
        exx = (PRIVATE/'source/exx.f90').read_text()
        resource = exx.split('SUBROUTINE qe75_capture_fft(fock)', 1)[1]
        self.assertLess(resource.index('CALL resource_write'), resource.index('CALL native_phase(5)'))
        ace = exx.split('  SUBROUTINE aceinit(', 1)[1].split('  END SUBROUTINE aceinit', 1)[0]
        self.assertLess(ace.index('CALL mp_sum( eexx'), ace.index('CALL native_phase(6)'))
        self.assertLess(ace.index('CALL native_phase(6)'), ace.index("CALL errore('r07_first_ace'"))
        store = exx.split('  SUBROUTINE qbridge_request_store(', 1)[1].split('  END SUBROUTINE', 1)[0]
        self.assertIn('CALL native_phase(7)', store)
        self.assertNotIn("qbridge_transaction('retire_operator')", store)
        self.assertIn('qs_extent(nr,lo,hi,nq)', store)
        report = json.loads((PRIVATE/'build.json').read_text())
        self.assertTrue(all(report['source']['native_arithmetic_byte_equal'].values()))
        self.assertFalse(report['QE_MPI_executed'])
    def test_phase_failure_reduced_before_barrier_no_signed_status_masking(self):
        for stage in [4, 5, 6, 7, 9]:
            for local, remote in [(0, 0), (-2147483648, 0), (0, 1)]:
                env = dict(os.environ, TEST_LOCAL_STATUS=str(local), TEST_REMOTE_FAILURE=str(remote))
                r = subprocess.run([str(self.root/'phase_model'), str(stage)], env=env,
                                   capture_output=True, text=True, timeout=3)
                success = stage in [4, 5, 6, 7] and local == remote == 0
                self.assertEqual(r.returncode == 0, success)
                self.assertEqual('SERIAL_MODEL_BARRIER' in r.stdout, success)
    def wire(self, stage, reply_scope, bad_nonce=False, status=0):
        address = 'r07-pair-serial-'+os.urandom(12).hex()
        lock = self.dir/'test-only.lock'
        fd = os.open(lock, os.O_CREAT|os.O_RDWR, 0o600); fcntl.flock(fd, fcntl.LOCK_EX)
        server = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
        server.bind('\0'+address); server.listen(1); server.settimeout(3)
        errors = []
        def reply():
            try:
                c,_ = server.accept()
                with c:
                    request = c.recv(181)
                    self.assertEqual(len(request), 180)
                    self.assertEqual(struct.unpack('!5I', request[:20]), (0x5230374c, 1, stage, 0, 2))
                    nonce = bytes(32) if bad_nonce else request[148:]
                    c.send(b'R07L'+struct.pack('!3I', 1, status, reply_scope)+nonce)
            except BaseException as e: errors.append(str(e))
        thread = threading.Thread(target=reply); thread.start()
        ticks = Path(f'/proc/{os.getpid()}/stat').read_text().rsplit(')', 1)[1].split()[19]
        env = dict(os.environ, QE75_LEASE_SOCKET=address, QE75_LEASE_PID=str(os.getpid()),
                   QE75_LEASE_TICKS=ticks, QE75_LEASE_LOCK=str(lock),
                   QE75_JOB_SHA256='a'*64, QE75_PROFILE_SHA256='b'*64)
        r = subprocess.run([str(self.root/'wire_worker'), str(stage), '4'], env=env,
                           capture_output=True, text=True, timeout=4)
        thread.join(4); server.close(); os.close(fd)
        self.assertFalse(thread.is_alive()); self.assertEqual(errors, [])
        return r
    def test_compiled_wire_nonce_scope_and_status_no_MPI(self):
        for stage in [4, 5, 6, 7]: self.assertEqual(self.wire(stage, 4).returncode, 0)
        for scope in [1, 2, 3]: self.assertNotEqual(self.wire(4, scope).returncode, 0)
        self.assertNotEqual(self.wire(5, 4, bad_nonce=True).returncode, 0)
        self.assertNotEqual(self.wire(6, 4, status=2**31).returncode, 0)
        # No owner/lock/environment yields strict refusal, not a fake grant.
        r = subprocess.run([str(self.root/'wire_worker'), '4', '4'], env={},
                           capture_output=True, text=True, timeout=3)
        self.assertNotEqual(r.returncode, 0)
    def test_historical_evidence_cannot_be_substituted_or_promoted(self):
        events = json.loads((HERE/'smoke_journal.json').read_text())
        r = verify(events); self.assertEqual(r['memory_peak_bytes'], 12890112)
        changed = json.loads(json.dumps(events)); changed[0]['USER_INVOCATION_ID'] = '0'*32
        with self.assertRaises(ValueError): verify(changed)
        evidence = json.loads((HERE/'smoke_verification.json').read_text())
        self.assertFalse(evidence['user_reported_rank_output']['persisted_stdout_recovered'])
        self.assertFalse(evidence['hostwide_MPI_absence_proven'])


if __name__ == '__main__':
    r = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PairTests))
    result = dict(passed=r.wasSuccessful(), methods=r.testsRun,
                  build_records=getattr(PairTests, 'build_records', []),
                  real_C_Unix_wire_tested=True, Fortran_collective_tests='SERIAL STUBS ONLY',
                  native_MPI_QE_started=False, native_phase_authority_issued=False,
                  synthetic_packet_tests_are_not_material_or_native_QE_validation=True,
                  failures=[str(e) for _,e in r.errors+r.failures])
    (HERE/'test_results.json').write_text(json.dumps(result, indent=2)+'\n')
    raise SystemExit(0 if r.wasSuccessful() else 1)
