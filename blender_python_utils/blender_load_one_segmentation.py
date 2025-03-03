
import numpy as np

import bpy
from bpy_extras.object_utils import AddObjectHelper, object_data_add

xy_scale = 0.01
z_scale = 0.01
axes_order = 'zyx'
thresh = 64

init_scale = 0.02
scale = np.array([1, 1, z_scale / xy_scale]) * init_scale

mesh_data = np.load('/g/icem/hennies/projects/kors/blender/dT_chromosomes/blender_inputs/chromosomes.npz')
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

