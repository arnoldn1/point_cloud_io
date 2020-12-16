from pathlib import Path
import numpy as np

from .type_aliases import FilePath, ReturnTypes, rtypes
from .converters import to_pd, to_np, to_pcd
from .extentions import io_las, io_o3d, io_serialising, io_txt


def read(file_path: FilePath, return_type='numpy', verbose=False, **kwargs) -> ReturnTypes:
    """Load point cloud data object from file path

    Available return types:

    `'numpy'` - Returns a :class:`numpy.ndarray`.
        The first 3 columns will be `x,y,z` followed by `r,g,b` if provided.
    `'pandas'` - Returns a pandas Dataframe.
        The columns names will be ['x', 'y', 'z'] and ['r', 'g', 'b'], if provided.
    `'o3d'` -  Returns a open3d PointCloud object.
        Contains points and colour, if provided.

    :param file_path: File str path or pathlib Path object.
    :param return_type: {'numpy', 'pandas', 'o3d'}, default 'numpy'.
    :param verbose: Control if print messages should be shown.
    :param kwargs: Additional keywords passed the underlying data writer.
    :return: Point cloud data object as specified return type, default 'numpy'.
    """
    if return_type not in rtypes.keys():
        raise ValueError(f'Return type {return_type} not recognised.\n'
                         f'Valid return types are {", ".join(rtypes.keys())}')
    file_path = Path(file_path)
    suffix = file_path.suffix

    # las formats
    if suffix in [k['format'] for k in io_las.extensions.values()]:
        obj = io_las.read_file(file_path)
        if obj[1].size > 0:
            obj = np.hstack((obj[0], obj[1]))
        else:
            obj = obj[0]

    # o3d formats
    elif suffix in [k['format'] for k in io_o3d.extensions.values()]:
        obj = io_o3d.read_file(file_path)

    # txt format
    elif suffix in [k['format'] for k in io_txt.extensions.values()]:
        obj = io_txt.read_file(file_path, **kwargs)

    # serialising formats
    elif suffix in [k['format'] for k in io_serialising.extensions.values()]:
        raise NotImplemented(f'File with type {suffix} not implemented.')

    else:
        raise NotImplemented(f'File with type {suffix} not implemented.')

    if return_type == 'numpy':
        obj = to_np(obj)
    elif return_type == 'pandas':
        obj = to_pd(obj)
    elif return_type == 'o3d':
        obj = to_pcd(obj)
    else:
        raise ValueError

    return obj


def write(obj: ReturnTypes, file_path: FilePath, verbose=False, **kwargs) -> Path:
    """
    Save point cloud data to file.

    :param obj: Point cloud data object.
    :param file_path: File str path or pathlib.Path object.
    :param verbose: Control if print messages should be shown.
    :param kwargs: kwargs: Additional keywords passed the underlying data reader.
    :return: Resolved path to data file.
    """
    file_path = Path(file_path)
    suffix = file_path.suffix

    # las formats
    if suffix in [k['format'] for k in io_las.extensions.values()]:
        obj = to_np(obj)
        final_path = io_las.write_obj(file_path, obj[:, :3], obj[:, 3:], **kwargs)

    # o3d formats
    elif suffix in [k['format'] for k in io_o3d.extensions.values()]:
        obj = to_pcd(obj)
        final_path = io_o3d.write_obj(obj, file_path, ext=suffix, **kwargs)

    # txt format
    elif suffix in [k['format'] for k in io_txt.extensions.values()]:
        obj = to_pd(obj)
        final_path = io_txt.write_obj(obj, file_path, **kwargs)

    # serialising formats
    elif suffix in [k['format'] for k in io_serialising.extensions.values()]:
        raise NotImplemented(f'File with type {suffix} not implemented.')

    else:
        raise NotImplemented(f'File with type {suffix} not implemented.')

    if verbose:
        print(f'Point cloud data saved to {final_path}')

    return final_path
