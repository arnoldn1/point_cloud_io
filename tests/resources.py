import numpy as np
from pathlib import Path

# temp directory for read / write
tmp_dir = Path('tmp_test_dir')
rng = np.random.default_rng()


def cleanup():
    files = tmp_dir.glob('*')
    for f in files:
        f.unlink(missing_ok=True)
    tmp_dir.rmdir()