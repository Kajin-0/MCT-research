# One bounded admission-domain assessment — HARD_BLOCKED for native launch

The existing foreground guardian can certify an observed pidfd descendant
family and exclude other cooperating owners using the kernel flock. Neither
certificate covers a foreign process that does not take that lock. Moving the
test into a private PID namespace would hide, rather than certify, host-wide
foreign MPI activity. It would not meet the original admission condition.

An authoritative alternative would need an enforced host admission boundary or
a trusted inventory of the unreadable identities. No such broker/mandatory
domain is provided by the existing inputs. The retained snapshot has EACCES
for PID 1 and other live mappings; familiar comm/UID values are not mapping
contents. Hidden MPI and no-MPI mappings can have identical exposed metadata.
Therefore the present observations cannot distinguish the two cases.

**HARD_BLOCKED:** no permission-compatible authoritative global certificate can
be constructed from these observations. No namespace, privileged broker,
permission change, process signal or new inventory search is attempted.
The native gate remains closed. Under `339265a`, proceed independently to the
common-state protocol, resource bounds and source-level readback/collectives.
