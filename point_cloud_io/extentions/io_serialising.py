import pickle
import pandas as pd
from pathlib import Path
from typing import Any
from ..type_aliases import FilePath, ArrayTuple, DataFrame, ReturnTypes
from ..converters import to_pd

extensions = {'pickle': {'format': '.pkl',
                         'description': 'Python Pickle'},
              'feather': {'format': '.feather',
                          'description': 'PyArrow binary Feather format'},
              'hdf5': {'format': '.h5',
                       'description': 'Hierarchical Data Format (HDF)'}}


def write_pickle(obj: ReturnTypes, file_path: FilePath, protocol=pickle.HIGHEST_PROTOCOL):
    file_path = Path(file_path).with_suffix(extensions['pickle']['format'])
    with open(str(file_path), 'wb') as f:
        pickle.dump(obj, f, protocol)


def read_pickle(file_path: FilePath) -> ReturnTypes:
    file_path = Path(file_path)
    with open(str(file_path), 'rb') as f:
        data = pickle.load(f)
    return data


def write_feather(obj: ReturnTypes, file_path: FilePath, **kwargs):
    file_path = Path(file_path).with_suffix(extensions['feather']['format'])
    obj = to_pd(obj)
    obj.to_feather(file_path, **kwargs)


def read_feather(file_path: FilePath, **kwargs) -> DataFrame:
    file_path = Path(file_path)
    obj = pd.read_feather(file_path, **kwargs)
    return obj


def write_hdf(obj: ReturnTypes, file_path: FilePath, key='pcd', **kwargs):
    file_path = Path(file_path).with_suffix(extensions['hdf5']['format'])
    obj = to_pd(obj)
    obj.to_hdf(file_path, key=key, **kwargs)


def read_hdf(file_path: FilePath, **kwargs) -> Any:
    file_path = Path(file_path)
    obj = pd.read_hdf(file_path, **kwargs)
    return obj
