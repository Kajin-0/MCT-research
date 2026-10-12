"""Owned exec stub: parent-death setup before launcher exec, no shell."""
import os
from pathlib import Path
import signal
import sys
from process_identity import parent_death

parent=int(sys.argv[1]);parent_death(signal.SIGKILL,parent)
os.execvpe(sys.argv[2],sys.argv[2:],os.environ)
