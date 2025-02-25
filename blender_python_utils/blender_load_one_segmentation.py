
import numpy as np
# from skimage.measure import marching_cubes

import bpy
from bpy_extras.object_utils import AddObjectHelper, object_data_add
# from h5py import File

# with File('/media/julian/Data/projects/hennies/blender/inputs/hela_er_ds4_g1.2.h5', mode='r') as f:
#     maskchannel = f['data'][:]

xy_scale = 0.01
z_scale = 0.01
axes_order = 'zyx'
thresh = 64

init_scale = 0.02
scale = np.array([1, 1, z_scale / xy_scale]) * init_scale

# obj_array = np.moveaxis(maskchannel, [axes_order.find('x'), axes_order.find('y'), axes_order.find('z')], [0, 1, 2])

# verts, faces, normals, values = marching_cubes(obj_array, thresh)

mesh_data = np.load('/g/schwab/Suzan/ilastik/dT_chromosomes/blender_inputs/chromosomes.npz')
verts, faces = mesh_data['verts'], mesh_data['faces']


mesh = bpy.data.meshes.new('er_ds4_g1.2')
mesh.from_pydata(verts, [], faces)
object_data_add(bpy.context, mesh)
obj = bpy.context.view_layer.objects.active
obj.location = [0, 0, 0]
obj.scale = scale
obj = bpy.context.active_object
attribute = obj.data.attributes.new(name="object id", type="INT", domain="POINT")
attribute.data.foreach_set('value', [0] * len(verts))

