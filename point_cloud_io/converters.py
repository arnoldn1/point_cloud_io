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
        pd_keys = list(obj.keys())
        # check rgb
        rgb_keys = ['r', 'g', 'b']
        if all([k in pd_keys for k in rgb_keys]):
            pcd.colors = o3d.utility.Vector3dVector(obj[rgb_keys].to_numpy())
            return pcd
        # check rgb floats
        rgbf_keys = ['rf', 'gf', 'bf']
        if all([k in pd_keys for k in rgbf_keys]):
            pcd.colors = o3d.utility.Vector3dVector(obj[rgbf_keys].to_numpy())
            return pcd

        if rgb is None:
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
        # check xyz values
        xyz_keys = ['x', 'y', 'z']
        if all([k in pd_keys for k in xyz_keys]):
            xyz = obj[xyz_keys].to_numpy()

        # check rgb values
        rgb_keys = ['r', 'g', 'b']
        if all([k in pd_keys for k in rgb_keys]):
            rgb = obj[rgb_keys].to_numpy()
            if not all([k in pd_keys for k in 'xyz']):
                return rgb

        # check rgb float values
        rgbf_keys = ['rf', 'gf', 'bf']
        if all([k in pd_keys for k in rgbf_keys]):
            rgb = obj[rgbf_keys].to_numpy()
            if not all([k in pd_keys for k in 'xyz']):
                return rgb

        if rgb is None:
            return xyz

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
