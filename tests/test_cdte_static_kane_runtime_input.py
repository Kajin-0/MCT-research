import hashlib
from pathlib import Path


def test_committed_runtime_win_hash():
    path = Path("first_principles/a0/cdte_static_kane_smoke_inputs/cdte_kane.runtime.win")
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == "58b9b9253084f5fef8a0f0aeecb22177278e78040826f64a4de79364379eedb4"
    assert data.decode().count("mp_grid = 13 1 1") == 1
