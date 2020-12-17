import pandas as pd
from pathlib import Path
from ..type_aliases import FilePath, ArrayTuple, DataFrame

extensions = dict(txt={'format': '.txt',
                       'description': 'Use Pandas for .txt file.',
                       'delimiter': ','},
                  asc={'format': '.asc',
                       'description': 'Use Pandas for CloudCompare style .asc file.',
                       'delimiter': ' '})


def write_obj(obj: DataFrame, file_path: FilePath, delimiter: str = None, index=False, **kwargs):
    """Save :class:`DataFrame` point cloud data to file path.

    For **.txt** files, assumes first row to be header with column names and uses ``delimiter=','``.

    For **.asc**, files are assumed to have a header from
    `CloudCompare ascii <https://www.cloudcompare.org/doc/wiki/index.php?title=ASCII_file_open_dialog>`_
    save defaults. The header row is preceded by `'//'` and defaults ``delimiter=' '``.

    :param delimiter: Overrides default file type delimiter
    """
    suffix = file_path.suffix
    file_type = suffix.strip('.')
    file_path = Path(file_path).with_suffix(extensions[file_type]['format'])
    delimiter = extensions[file_type]['delimiter'] if delimiter is None else delimiter
    if file_type == 'asc' and ('header' not in kwargs.keys()):
        kwargs['header'] = ('//' + ','.join(obj.keys())).split(',')

    obj.to_csv(file_path, sep=delimiter, index=index, **kwargs)
    return file_path.resolve()


def read_file(file_path: FilePath, delimiter=None, header=0, dropna=True, **kwargs) -> DataFrame:
    """Load point cloud data from .txt or .asc file.

    For **.txt** files, assumes first row to be header with column names and uses ``delimiter=','``.

    For **.asc**, files are assumed to have a header from
    `CloudCompare ascii <https://www.cloudcompare.org/doc/wiki/index.php?title=ASCII_file_open_dialog>`_
    save defaults. Defaults to ``delimiter=' '`` and strips `'//'` from header if present.

    :param delimiter: Overrides default file type delimiter
    """
    suffix = file_path.suffix
    file_type = suffix.strip('.')
    delimiter = extensions[file_type]['delimiter'] if delimiter is None else delimiter

    if dropna:
        data = pd.read_csv(str(file_path), delimiter, header=header).dropna()
    else:
        data = pd.read_csv(str(file_path), delimiter, header=header, **kwargs)

    data.columns = data.columns.str.lower()
    if file_type == 'asc':
        header = ','.join(data.keys())
        if '//' in header:
            data.columns = header.strip('//').split(',')
    return data
