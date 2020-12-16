import pandas as pd
from pathlib import Path
from ..type_aliases import FilePath, ArrayTuple, DataFrame

extensions = dict(txt={'format': '.txt',
                        'description': 'Use Pandas to save to txt file.'})


def write_obj(obj: DataFrame, file_path: FilePath, delimiter=' ', **kwargs):
    """Save :class:`DataFrame` point cloud data to file path."""
    file_path = Path(file_path).with_suffix(extensions['txt']['format'])
    obj.to_csv(file_path, sep=delimiter, **kwargs)
    return file_path.resolve()


def read_file(file_path: FilePath, delimiter=' ', header=0, dropna=True, **kwargs) -> DataFrame:
    """Load point cloud data from .txt file."""
    if dropna:
        data = pd.read_csv(str(file_path), delimiter, header=header).dropna()
    else:
        data = pd.read_csv(str(file_path), delimiter, header=header, **kwargs)

    data.columns = data.columns.str.lower()
    return data
