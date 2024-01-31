"""
Use this script to load multiple split label volumes into blender (outputs of split_segmentation.py)

Use this script directly in the Blender Scripting tab.
"""

import json

import bpy
import pyopenvdb as openvdb
import os
import numpy as np

source_folder = '/media/julian/Data/projects/khan/blender/data/labels_t69'
pixel_spacing = np.array((0.6, 0.042, 0.042))
json_fp = os.path.join(source_folder, 'pos.json')
obj_fp = os.path.join(source_folder, 'obj_{:06d}.npy')

with open(json_fp, 'r') as f:
    positions = json.load(f)

for idx, pos in positions.items():

    lbl = int(idx) + 1

    obj = np.load(obj_fp.format(lbl))
    grid = openvdb.FloatGrid()
    grid.copyFromArray(obj.astype(float))

    grid.transform = openvdb.createLinearTransform(
        [
            [pixel_spacing[0], 0, 0, 0],
            [0, pixel_spacing[1], 0, 0],
            [0, 0, pixel_spacing[2], 0],
            [pos[0], pos[1], pos[2], 1]
        ]
    )

    grid.gridClass = openvdb.GridClass.FOG_VOLUME
    grid.name = 'density'

    this_vdb_fp = os.path.join(source_folder, os.path.splitext(obj_fp.format(lbl))[0] + '.vdb')
    openvdb.write(this_vdb_fp, grid)
    bpy.ops.object.volume_import(filepath=this_vdb_fp, files=[])

