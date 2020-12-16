import numpy as np
from laspy.file import File
from laspy.header import Header
from laspy.util import LaspyException
from pathlib import Path
from ..type_aliases import FilePath, ndarray, ArrayTuple

extensions = dict(las={'format': '.las',
                       'description': 'LAS file format'},
                  laz={'format': '.laz',
                       'description': 'LAZ compressed file format'})


def read_file(file_path: FilePath) -> ArrayTuple:
    """Read .las file."""
    file_path = Path(file_path)
    if file_path.suffix not in [k['format'] for k in extensions.values()]:
        raise NotImplementedError

    xyz = np.empty(0)
    rgb = np.empty(0)

    with File(str(file_path), mode='r') as f:
        xyz = np.array((f.x, f.y, f.z)).T
        try:
            if hasattr(f, 'red') and hasattr(f, 'green') and hasattr(f, 'blue'):
                rgb = np.array((f.red, f.green, f.blue)).T
        except LaspyException:
            pass

    return xyz, rgb


def write_obj(file_path: FilePath, xyz: ndarray, rgb: ndarray = None, scale: float = 1e-05):
    """Write :param:`xyz` and :param:`rgb` to .las file."""
    file_path = Path(file_path).with_suffix(extensions['las']['format'])
    point_format = 0

    if rgb is not None and rgb.shape[1] > 0:
        if xyz.shape != rgb.shape:
            raise ValueError(f'xyz and rgb shape must match.\n'
                             f'Got {xyz.shape} and {rgb.shape}')
        point_format = 2
    header = Header(point_format=point_format)

    with File(str(file_path), mode="w", header=header) as f:

        f.header.scale = (scale, scale, scale)

        f.header.offset = np.min(xyz, axis=0)
        f.x = xyz[:, 0]
        f.y = xyz[:, 1]
        f.z = xyz[:, 2]
        if rgb is not None and rgb.shape[1] > 0:
            f.red = rgb[:, 0] * 2 ** 8
            f.green = rgb[:, 1] * 2 ** 8
            f.blue = rgb[:, 2] * 2 ** 8

    return file_path.resolve()
