"""Prospective terminal FD handling. No native launch entry point or JSON authority.

A vanished /proc path or Z state never proves exit. Only pinned process pidfds
(flags=0, not PIDFD_THREAD) do. Live wire receipts are constructed here rather
than loaded from previous evidence. RefUnit retains manager exit metadata.
"""
import ctypes
import os
from pathlib import Path
import select
import socket
import struct
import sys

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'cgroup_owned_2026-10-13'))
from contracts import show, own_cgroup, cgroup_path
from process_identity import proc, Refusal

SO_PEERPIDFD = 77  # Linux UAPI asm-generic/socket.h; no fallback if unsupported.


class TerminalPending(Refusal):
    """Exit proved, final receipts complete; inventory still NOT accepted."""


def exit_events(fd):
    poller = select.poll()
    poller.register(fd, select.POLLIN)
    events = poller.poll(0)
    mask = events[0][1] if events else 0
    if mask & ~(select.POLLIN | select.POLLHUP):
        raise Refusal('invalid/error pidfd; no exit certificate')
    return mask


class Peer:
    def __init__(self, conn, expected_uid, expected_cgroup):
        self.fd = None
        peerfd = None
        try:
            pid, uid, _ = struct.unpack('3i', conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
            if uid != expected_uid:
                raise Refusal('foreign kernel peer UID')
            # Tied to the actual connecting task, even if its numeric PID reuses.
            peerfd = conn.getsockopt(socket.SOL_SOCKET, SO_PEERPIDFD)
            if exit_events(peerfd):
                raise Refusal('socket peer already exited during acquisition')
            before = proc(pid)
            if own_cgroup(pid) != expected_cgroup:
                raise Refusal('foreign kernel peer cgroup')
            self.fd = os.pidfd_open(pid, 0)
            after = proc(pid)
            if before['start_ticks'] != after['start_ticks']:
                raise Refusal('PID reuse during acquisition')
            # Exit is irreversible. A STILL LIVE socket-bound pidfd after open
            # proves the original peer lived throughout the numeric open interval.
            if exit_events(peerfd) or exit_events(self.fd):
                raise Refusal('peer exited during numeric pidfd binding')
            info = Path(f'/proc/self/fdinfo/{self.fd}').read_text().splitlines()
            if int(next(v.split()[1] for v in info if v.startswith('Pid:'))) != pid:
                raise Refusal('pidfd namespace/PID mismatch')
            self.pid, self.start_ticks = pid, after['start_ticks']
            self.cgroup = expected_cgroup
            s = os.fstat(self.fd)
            self.fd_identity = (s.st_dev, s.st_ino)
        except BaseException:
            self.close()
            raise
        finally:
            if peerfd is not None:
                os.close(peerfd)

    def exited(self):
        if self.fd is None:
            raise Refusal('closed/unbound pidfd')
        s = os.fstat(self.fd)
        if (s.st_dev, s.st_ino) != self.fd_identity:
            raise Refusal('pidfd descriptor reused')
        return bool(exit_events(self.fd))

    def live_identity(self):
        if self.exited():
            raise Refusal('registered peer exited')
        row = proc(self.pid)
        if row['start_ticks'] != self.start_ticks or own_cgroup(self.pid) != self.cgroup:
            raise Refusal('registered PID replaced/moved')
        if self.exited():
            raise Refusal('registered peer exited during live check')
        return row

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None


class UnitReference:
    """Persistent connection-local RefUnit; no globals/property changes."""
    def __init__(self, unit):
        self.unit = unit
        self.bus = ctypes.c_void_p()
        self.lib = ctypes.CDLL('libsystemd.so.0')
        self.lib.sd_bus_new.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.sd_bus_new.restype = ctypes.c_int
        self.lib.sd_bus_set_address.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.sd_bus_set_address.restype = ctypes.c_int
        self.lib.sd_bus_set_bus_client.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.lib.sd_bus_set_bus_client.restype = ctypes.c_int
        self.lib.sd_bus_start.argtypes = [ctypes.c_void_p]
        self.lib.sd_bus_start.restype = ctypes.c_int
        self.lib.sd_bus_unref.argtypes = [ctypes.c_void_p]
        self.lib.sd_bus_unref.restype = ctypes.c_void_p
        self.lib.sd_bus_call_method.restype = ctypes.c_int
        # Fixed arguments precede the C varargs 's' string.
        self.lib.sd_bus_call_method.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
            ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_char_p]
        self.lib.sd_bus_set_method_call_timeout.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
        self.lib.sd_bus_set_method_call_timeout.restype = ctypes.c_int
        try:
            if os.getuid() != 1001:
                raise Refusal('fixed UID1001 user bus required')
            code = self.lib.sd_bus_new(ctypes.byref(self.bus))
            if code < 0:
                raise Refusal('user bus unavailable errno ' + str(-code))
            for code in (self.lib.sd_bus_set_address(self.bus, b'unix:path=/run/user/1001/bus'),
                         self.lib.sd_bus_set_bus_client(self.bus, 1), self.lib.sd_bus_start(self.bus)):
                if code < 0:
                    raise Refusal('explicit user bus connect errno ' + str(-code))
            if self.lib.sd_bus_set_method_call_timeout(self.bus, 2_000_000) < 0:
                raise Refusal('bounded user bus deadline unavailable')
            self.call('RefUnit')
        except BaseException:
            self.close()
            raise

    def call(self, method):
        code = self.lib.sd_bus_call_method(self.bus, b'org.freedesktop.systemd1',
            b'/org/freedesktop/systemd1', b'org.freedesktop.systemd1.Manager',
            method.encode(), None, None, b's', self.unit.encode())
        if code < 0:
            raise Refusal(method + ' failed errno ' + str(-code))

    def close(self):
        if self.bus:
            self.lib.sd_bus_unref(self.bus)
            self.bus = ctypes.c_void_p()


class Retirement:
    def __init__(self, unit, invocation, cgroup, job, profile):
        f = show(unit)
        if f['Id'] != unit or f['InvocationID'] != invocation or f['ActiveState'] != 'active':
            raise Refusal('initial manager invocation inactive/mismatched')
        if f['ControlGroup'] != cgroup or f['Restart'] != 'no' or f['Delegate'] != 'no':
            raise Refusal('initial manager cgroup/lifecycle mismatch')
        self.unit, self.invocation, self.cgroup = unit, invocation, cgroup
        self.cg = cgroup_path(cgroup)
        s = self.cg.stat()
        self.cg_identity = (s.st_dev, s.st_ino)
        self.job, self.profile = job, profile
        self.ranks, self.final = {}, {}
        self.reference = UnitReference(unit)

    def receipt(self, conn, rank, action, job, profile):
        # Call only after the existing native wire extent/nonce, ELF/argv,
        # lineage, lease and numerical readback checks. No receipts from JSON.
        if rank not in (0, 1) or action not in (1, 10) or (job, profile) != (self.job, self.profile):
            raise Refusal('typed final receipt mismatch')
        peer = Peer(conn, os.getuid(), self.cgroup)
        try:
            if action == 1:
                if rank in self.ranks or peer.pid in [p.pid for p in self.ranks.values()]:
                    raise Refusal('duplicate/replaced rank registration')
                self.ranks[rank] = peer
                peer = None
            else:
                if set(self.ranks) != {0, 1} or rank in self.final:
                    raise Refusal('unregistered/duplicate final receipt')
                pinned = self.ranks[rank]
                pinned.live_identity()
                if (peer.pid, peer.start_ticks) != (pinned.pid, pinned.start_ticks):
                    raise Refusal('final receipt from different kernel task')
                self.final[rank] = dict(pid=peer.pid, start_ticks=peer.start_ticks,
                    invocation=self.invocation, cgroup=self.cgroup, job=job, profile=profile)
        finally:
            if peer is not None:
                peer.close()

    def inventory_failure(self, pid, error):
        matches = [v for v in self.ranks.values() if v.pid == pid]
        if len(matches) != 1 or set(self.final) != {0, 1}:
            raise Refusal('FD inventory incomplete before authenticated final pair') from error
        if not matches[0].exited():
            raise Refusal('FD inventory denied/missing for STILL LIVE registered task') from error
        # NO omission authority yet: transition out of active sampling and wait
        # boundedly for all pidfds, manager exit0 and empty cgroup. Host pressure,
        # tree/output samples and hard limits must continue in the owner.
        raise TerminalPending('kernel exit proved; complete terminal gate pending') from error

    def terminal(self, wait_client):
        if set(self.final) != {0, 1} or not all(p.exited() for p in self.ranks.values()):
            raise Refusal('terminal ranks incomplete/still live')
        f = show(self.unit)
        expected = dict(Id=self.unit, LoadState='loaded', InvocationID=self.invocation,
            ActiveState='inactive', SubState='dead', Result='success', ExecMainCode='1',
            ExecMainStatus='0', MainPID='0', Restart='no', Delegate='no')
        if any(f.get(k) != v for k, v in expected.items()) or wait_client.poll() != 0:
            raise Refusal('terminal manager/foreground wait not matching clean exit0')
        if self.cg.exists():
            s = self.cg.stat()
            if (s.st_dev, s.st_ino) != self.cg_identity:
                raise Refusal('terminal cgroup path reused')
            events = dict(v.split() for v in (self.cg / 'cgroup.events').read_text().splitlines())
            leaves = [self.cg, *[v for v in self.cg.rglob('*') if v.is_dir()]]
            if events.get('populated') != '0' or any((v/'cgroup.procs').read_text().strip() for v in leaves):
                raise Refusal('terminal cgroup still populated/unreadable')
        # Absent cgroup alone never grants authority: all prior conditions hold.
        return dict(kernel_all_pinned_ranks_exited=True, final_receipts=list(self.final.values()),
            manager=f, cgroup_empty=True, kernel_cgroup_identity=self.cg_identity,
            no_proc_status_or_missing_PID_authority=True, omission_eligible_only_after_final_gate=True)

    def close(self):
        for peer in self.ranks.values():
            peer.close()
        self.reference.close()
