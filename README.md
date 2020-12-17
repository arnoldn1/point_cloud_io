# Point Cloud IO - pcio
Point_cloud_io `pcio` is a python library for reading and writting point cloud data.

## Description
Written as a convenience wrapper of 
[Open3D](https://github.com/intel-isl/Open3D), 
[Pandas](https://pandas.pydata.org/) and 
[Laspy](https://github.com/grantbrown/laspy) 
to streamline reading, writing and converting between point clouds of different file formats.
See [Dev](Dev) section for supported file type formats. 


Tested using Python 3.8

### License
This project is released under GNU General Public License.

### Install
clone repo:\
`$ git clone ...`

change into directory\
`$ cd point_cloud_io`

install in development mode through pip\
`$ pip install -e .`

### Usage
```python
import point_cloud_io as pcio
import numpy as np

xyz = np.random.default_rng().random((100, 3))
# file type will be inferred by the file extension, i.e., .xyz
pcio.write(xyz, 'path/to/file.xyz')

# return_type indicates how the read object should be return, 
# e.g., 'numpy' returns a np.array
xyz = pcio.read('path/to/file.xyz', return_type='numpy')    
```

See `tests` for more examples

Available return types:
- `'numpy'` 
returns a numpy array, first 3 columns will be [x,y,z] followed by [r,g,b] if provided.
- `'pandas'` 
returns a pandas Dataframe, columns names will be ['x', 'y', 'z'] and ['r', 'g', 'b'], if provided.
- `'o3d'` 
returns a open3d PointCloud object containing points and colour, if provided.

### Note about .txt and .asc files
For `.txt` files, assumes first row to be header with column names and uses `','` as delimiter.
 
Similarly, the first row of `.asc` files are assumed to have a header from CloudCompare ascii save default.
The header row is preceded by `'//'` and uses `' '` as a delimiter.

Default delimiters can be overridden using `delimiter=` keyword.

## Dev
Implementation list:
- [x] .las      (laspy)
- [ ] .laz      (laspy)
- [x] .xyz      (open3d)
- [ ] .xyzn     (open3d)
- [x] .xyzrgb   (open3d)
- [x] .pts      (open3d)
- [x] .ply      (open3d)
- [x] .pcd      (open3d)
- [x] .txt      (pandas)
- [x] .asc      (pandas)
- [ ] .pickle   (pickle)
- [ ] .feather  (pandas)
- [ ] .hdf5     (pandas)