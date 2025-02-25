# from h5py import File
import bpy
import pyopenvdb as openvdb
import os

# source = '/media/julian/Data/projects/khan/blender/data/raw_t69_c0.h5'
# proj_path = '/media/julian/Data/projects/khan/blender/data/'
#
# file_basename = os.path.splitext(os.path.split(source)[1])[0]
# target = os.path.join(proj_path, f'{file_basename}.vbd')
#
# with File(source) as f:
#     data = f['data'][:].astype('float') / 255

data = np.load('/g/schwab/Suzan')

grid = openvdb.FloatGrid()
grid.copyFromArray(data.astype(float))

grid.transform = openvdb.createLinearTransform([[0.032, 0, 0, 0], [0, 0.02, 0, 0], [0, 0, 0.02, 0], [0, 0, 0, 1]])

#grid.gridClass = openvdb.GridClass.FOG_VOLUME

grid.name = 'density'

openvdb.write(target, grid)
bpy.ops.object.volume_import(filepath=target, files=[])
