from pathlib import Path
from numpy import ndarray
from pandas import DataFrame
from open3d.cpu.pybind.geometry import PointCloud
from typing import Union, Tuple

rtypes = {'numpy': ndarray, 'o3d': PointCloud, 'pandas': DataFrame}
FilePath = Union[str, Path]
ReturnTypes = Union[ndarray, DataFrame, PointCloud]
xyz_or_rgb = Union[ndarray, Tuple[ndarray, ndarray]]
ArrayTuple = Tuple[ndarray, ndarray]
