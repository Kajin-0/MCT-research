"""Correct the missed outer-iteration export guard in private source only.

This is a refusal patch, not a native checkpoint implementation. No native run.
"""
from pathlib import Path
import argparse

def patch_source(path):
    path=Path(path).resolve()
    if not path.is_relative_to(Path('/home/User/opencode_workspace/DFT/.local').resolve()):
        raise ValueError('private source only')
    text=path.read_text()
    needle='     IF ( check_stop_now() .or. (iter.ge.nexxiter) ) THEN\n'
    if text.count(needle)!=1: raise ValueError('wrong/modified QE source')
    replacement=needle+'''#if defined(__EXX_QSTREAM)
        ! Both interruption paths refuse incomplete native state/checkpoint export.
        CALL errore('electrons','qstream native checkpoint bridge not qualified (outer stop)',1)
#endif
'''
    path.write_text(text.replace(needle,replacement,1))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('private_electrons_source',type=Path)
    patch_source(parser.parse_args().private_electrons_source)
