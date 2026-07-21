"""Shared reproducibility defaults for repository build tools.

Build entry points may override these values explicitly.  The defaults ensure
that subprocesses such as ``rsvg-convert`` emit deterministic PDF metadata when
the tools are invoked through ``python -m tools...`` or imported by tests.
"""

from __future__ import annotations

import os

os.environ.setdefault("SOURCE_DATE_EPOCH", "946684800")
os.environ.setdefault("FORCE_SOURCE_DATE", "1")
os.environ.setdefault("TZ", "UTC")
