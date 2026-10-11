# Decision: STOP_NO_NATIVE_STATE_BRIDGE

The finite phase establishes two useful software components: a versioned,
checksummed, no-copy checkpoint **storage ownership** transaction with a read-only
Fortran storage adapter, and strict 64-bit disk/quota/reservation/RAM/wall guard
primitives. Fifteen small test methods (including six publication fault points
and live-open Fortran ownership/restoration) plus all 24 storage regression cases
pass. C/Fortran source compiles. A corrective native-source refusal patch closes
the previously missed between-exchange-iterations export path.

**The requested full native checkpoint integration is not complete.** The exact
blocker is the absent audited capture/import bridge that ties old `xi`/source
occupations and HSE state to the current native SCF save at both interruption
points and after `punch`, across ranks, before destructive restart initialization.
Byte-valid stream/opaque sidecars and successful compilation do not establish
that closure. The backend therefore refuses native qualification by construction.
This is an implementation/validation NO-GO, not a proof that it is impossible.

**No native comparison is run.** The user authorized it only after source/state/
unit/guard gates pass. The native-state gate fails; running a fresh small HSE
fixture now would waive that sequential condition. Actual project-quota uncertainty
was resolved without privilege changes, so it is **not** used as a fabricated
remaining blocker. A small arithmetic resource admission passes; the original
nominal 22-GiB store fails the new 10-GiB disk reserve and is not allocated.

One next action is logically required: implement and independently validate the
native capture/import bridge described in `checkpoint_contract.md`. Then wire
reservation and owned-family runtime monitoring, and only if all gates pass use
the single retained comparison protocol. No queue, implicit new authorization,
hardware purchase, broad native campaign or empirical gap fitting is created.

Stock QE, the previous unexecuted private binary, dirty DFT files and all 17
protected source/supervisor pins are unchanged. Historical BLOCKED /goal and
material no-go results remain unchanged; physical t_H/gap/x_c remain absent.
Stop this phase at the explicit code-readiness boundary and push only validated
MCT artifacts to the existing research branch, without main merge or DFT commit.
