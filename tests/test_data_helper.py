import numpy as np
from pathlib import Path

import point_cloud_io as pcio
from resources import tmp_dir, rng, cleanup


def test_data_helper():
    # create fake data to test
    xyz = rng.random((100, 3))
    tmp_dir.mkdir(exist_ok=True)

    # save fake cloud to read in as different return types
    file_name = tmp_dir / Path('test_xyz.ply')
    # test writing xyz data as las
    pcio.write(xyz, file_name, verbose=True)

    # test reading ply file as numpy return type
    obj = pcio.read(file_name, return_type='numpy')
    assert isinstance(obj, pcio.data_helper.rtypes['numpy'])
    assert np.allclose(obj, xyz)
    del obj

    # test reading ply file as o3d return type
    obj = pcio.read(file_name, return_type='o3d')
    assert isinstance(obj, pcio.data_helper.rtypes['o3d'])
    del obj

    # test reading ply file as pandas return type
    obj = pcio.read(file_name, return_type='pandas')
    assert isinstance(obj, pcio.data_helper.rtypes['pandas'])
    del obj
    cleanup()
    return


def test_data_helper_rgb():
    # create fake data to test
    xyz = rng.random((100, 3))
    rgb = rng.uniform(low=0, high=1, size=xyz.shape)
    tmp_dir.mkdir(exist_ok=True)
    xyz_rgb = np.hstack((xyz, rgb))

    # save fake cloud to read in as different return types
    file_name = tmp_dir / Path('test_xyz_rgb.ply')
    # test writing xyz data as las
    pcio.write(xyz_rgb, file_name, verbose=True)

    # test reading ply file as numpy return type
    obj = pcio.read(file_name, return_type='numpy')
    assert isinstance(obj, pcio.data_helper.rtypes['numpy'])
    del obj

    # test reading ply file as o3d return type
    obj = pcio.read(file_name, return_type='o3d')
    assert isinstance(obj, pcio.data_helper.rtypes['o3d'])
    del obj

    # test reading ply file as pandas return type
    obj = pcio.read(file_name, return_type='pandas')
    assert isinstance(obj, pcio.data_helper.rtypes['pandas'])
    del obj
    cleanup()
    return


if __name__ == '__main__':
    test_data_helper()
    test_data_helper_rgb()
