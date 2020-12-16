import open3d as o3d
from pathlib import Path
from ..type_aliases import PointCloud, FilePath, ReturnTypes, rtypes

# Descriptions from Open3D documentation
# http://www.open3d.org/docs/release/tutorial/geometry/file_io.html
extensions = dict(xyz={'format': '.xyz',
                       'description': 'Each line contains [x, y, z], where x, y, z are the 3D coordinates'},
                  xyzn={'format': '.xyzn',
                        'description': 'Each line contains [x, y, z, nx, ny, nz], '
                                       'where nx, ny, nz are the normals'},
                  xyzrgb={'format': '.xyzrgb',
                          'description': 'Each line contains [x, y, z, r, g, b], '
                                         'where r, g, b are in floats of range [0, 1]'},
                  pts={'format': '.pts',
                       'description': 'The first line is an integer representing the number of points. '
                                      'Each subsequent line contains [x, y, z, i, r, g, b], where r, g, b are in uint8'},
                  ply={'format': '.ply',
                       'description': 'Polygon File Format, '
                                      'the ply file can contain both point cloud and mesh data'},
                  pcd={'format': '.pcd', 'description': 'Point Cloud Library file pcd file format'})


def read_file(file_path: FilePath) -> PointCloud:
    """Read point cloud data from as :class:`PointCloud`."""
    file_path = Path(file_path)
    if file_path.suffix not in [k['format'] for k in extensions.values()]:
        raise NotImplementedError

    pcd = o3d.io.read_point_cloud(str(file_path))
    return pcd


def write_obj(obj: PointCloud, file_path: FilePath, ext=extensions['ply']['format'], **kwargs):
    """Save :class:`PointCloud` point cloud data to file path."""
    file_path = Path(file_path).with_suffix(ext)
    o3d.io.write_point_cloud(str(file_path), obj, **kwargs)
    return file_path.resolve()
