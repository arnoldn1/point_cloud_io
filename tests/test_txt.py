import numpy as np
from pathlib import Path

import point_cloud_io as pcio
from resources import tmp_dir, rng, cleanup


# tests should return same thing given
def test_txt():
    # create fake data to test
    xyz = rng.random((100, 3))
    rgb = rng.uniform(low=0, high=1, size=xyz.shape)
    tmp_dir.mkdir(exist_ok=True)

    file_name = tmp_dir / Path('test_xyz.txt')
    # test writing xyz data as las
    pcio.write(xyz, file_name, verbose=True)
    # test reading las file
    new_xyz = pcio.read(file_name)
    assert np.allclose(xyz, new_xyz, atol=1e-05)

    xyz_rgb = np.hstack((xyz, rgb))
    file_name = tmp_dir / Path('test_xyz_rgb.txt')
    # test writing xyz data as las
    pcio.write(xyz_rgb, file_name, verbose=True)
    # test reading las file
    new_xyz_rgb = pcio.read(file_name)
    assert new_xyz_rgb.shape == xyz_rgb.shape
    # test xyz
    assert np.allclose(xyz_rgb[:, :3], new_xyz_rgb[:, :3], atol=1e-05)
    # test rgb
    assert np.allclose(xyz_rgb[:, 3:], new_xyz_rgb[:, 3:], atol=1e-0)

    cleanup()
    return


if __name__ == '__main__':
    test_txt()
