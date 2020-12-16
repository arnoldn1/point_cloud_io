import open3d as o3d
import numpy as np
import pandas as pd
from .type_aliases import ReturnTypes, PointCloud, rtypes, ndarray, DataFrame


# TODO: handle normals and others feature


def to_pcd(obj: ReturnTypes, rgb: ReturnTypes = None) -> PointCloud:
    """Convert to Open3d PointCloud object."""
    if isinstance(obj, rtypes['o3d']):
        return obj

    pcd = o3d.geometry.PointCloud()
    if isinstance(obj, rtypes['numpy']):
        pcd.points = o3d.utility.Vector3dVector(obj[:, :3])
        if rgb is None:
            if obj[:, 3:].shape == obj[:, :3].shape:
                pcd.colors = o3d.utility.Vector3dVector(obj[:, 3:])
            return pcd

    elif isinstance(obj, rtypes['pandas']):
        pcd.points = o3d.utility.Vector3dVector(obj[['x', 'y', 'z']].to_numpy())
        if all([k in list(obj.keys()) for k in 'rgb']):
            pcd.colors = o3d.utility.Vector3dVector(obj[['r', 'g', 'b']].to_numpy())
            return pcd
        elif rgb is None:
            return pcd
    else:
        raise NotImplementedError

    if rgb is not None:
        pcd.colors = o3d.utility.Vector3dVector(to_np(rgb))
        return pcd


def to_np(obj: ReturnTypes) -> ndarray:
    """Convert to numpy array.

    Array will always return in format [x, y, z, r, g, b]
    """
    xyz, rgb, others = None, None, None
    if isinstance(obj, rtypes['numpy']):
        return obj

    elif isinstance(obj, rtypes['pandas']):
        pd_keys = list(obj.keys())
        if all([k in pd_keys for k in 'xyz']):
            xyz = obj[['x', 'y', 'z']].to_numpy()
            if not all([k in pd_keys for k in 'rgb']):
                return xyz
        if all([k in pd_keys for k in 'rgb']):
            rgb = obj[['r', 'g', 'b']].to_numpy()
            if not all([k in pd_keys for k in 'xyz']):
                return rgb

    elif isinstance(obj, rtypes['o3d']):
        if obj.has_points():
            xyz = np.array(obj.points)
            if not obj.has_colors():
                return xyz
        if obj.has_colors():
            rgb = np.array(obj.colors)
            if not obj.has_points():
                return rgb
    else:
        raise NotImplementedError

    if (xyz is not None) and (rgb is not None):
        arr = np.hstack((xyz, rgb))
        return arr


def to_pd(obj: ReturnTypes) -> DataFrame:
    """Convert to pandas Dataframe.

    Columns will be ['x', 'y', 'z'] and ['r', 'g', 'b'], if color is provided.
    """
    if isinstance(obj, DataFrame):
        return obj

    xyz, rgb, others = None, None, None
    if isinstance(obj, PointCloud):
        if obj.has_points():
            xyz = np.array(obj.points)
            if not obj.has_colors():
                return pd.DataFrame({'x': xyz[:, 0],
                                     'y': xyz[:, 1],
                                     'z': xyz[:, 2]})
        if obj.has_colors():
            rgb = np.array(obj.colors)
            if not obj.has_points():
                return pd.DataFrame({'r': rgb[:, 0],
                                     'g': rgb[:, 1],
                                     'b': rgb[:, 2]})

    elif isinstance(obj, ndarray):
        xyz = obj[:, :3]
        rgb = obj[:, 3:]
        if rgb.shape != xyz.shape:
            return pd.DataFrame({'x': xyz[:, 0],
                                 'y': xyz[:, 1],
                                 'z': xyz[:, 2]})
    else:
        raise NotImplementedError

    return pd.DataFrame({'x': xyz[:, 0],
                         'y': xyz[:, 1],
                         'z': xyz[:, 2],
                         'r': rgb[:, 0],
                         'g': rgb[:, 1],
                         'b': rgb[:, 2]})
