"""Exact private accounting copy with fatal/pending FD-race routing; no jobs."""
from pathlib import Path
import ast
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'qe75_streaming_2026-10-11/terminal_owner_2026-10-14/sampled_output.py'
text=OLD.read_text().split('# NEW scope:')[0]
old='                except (FileNotFoundError,ProcessLookupError):continue'
assert text.count(old)==1
text=text.replace(old,"""                except (FileNotFoundError,ProcessLookupError) as error:
                    if self.retirement is None:
                        raise OutputRefusal('incomplete owned per-fd inventory') from error
                    self.retirement.inventory_failure(pid,error)""")
tree=ast.parse((HERE.parent/'static_environment_2026-10-15/owner.py').read_text())
node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Account')
text+='\nSingleMemberAccount=OutputAccount\n\n'+ast.get_source_segment((HERE.parent/'static_environment_2026-10-15/owner.py').read_text(),node)+'\n'
(HERE/'account.py').write_text(text)
