# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

__author__ = "code@kroko.me"

import sys
import bpy

def str_to_bool(s):
  return s.lower() in ("yes", "true", "t", "1")

argv = sys.argv
argv = argv[argv.index("--") + 1:]

# Print in console
print('Slave argument count: ' + str(len(argv)) )
print('Slave thread count: ' + str(argv[0]) )
print('Slave image save path: ' + str(argv[1]) )
print('Slave renderer to use: ' + str(argv[2]) )
print('Slave file format: ' + str(argv[3]) )
print('Slave overrides device: ' + str(argv[4]) )
print('Slave device: ' + str(argv[5]) )
print('Slave overrides tiles: ' + str(argv[6]) )
print('Slave Tile order: ' + str(argv[7]) )
print('Slave tile X: ' + str(argv[8]) )
print('Slave tile Y: ' + str(argv[9]) )
print('Slave frames to render: ')
frame_idx_begin = 10
frame_idx = frame_idx_begin
while frame_idx < len(argv):
   print( str(argv[frame_idx]) )
   frame_idx += 1

# Set vars
in_thread_count = int(argv[0]);
in_render_engine = argv[2];
in_save_path = argv[1];
in_save_file_format = argv[3];
in_save_override_device_active = str_to_bool(argv[4]);
in_save_override_device_type = argv[5];
in_save_override_tile_active = str_to_bool(argv[6]);
in_save_override_tile_tile_order = argv[7];
in_save_override_tile_tile_x = int(argv[8]);
in_save_override_tile_tile_y = int(argv[9]);

# Set scene as defined in Client, currently default
bpy.data.screens['Default'].scene = bpy.data.scenes['Scene']
bpy.context.screen.scene=bpy.data.scenes['Scene']

# Set rendering engine (specified by Client)
bpy.context.scene.render.engine = in_render_engine

# This can be overriden in Slave panel
# If not overriden, we use Client settings
if in_render_engine == 'CYCLES':
   if in_save_override_device_active:
      print('Slave overriding device for Cycles from ' + bpy.context.scene.cycles.device + ' to ' + in_save_override_device_type)
      bpy.context.scene.cycles.device = in_save_override_device_type
      # This is set by global settings on Slave, but might be overriden in Slave panel
      # bpy.context.user_preferences.system.compute_device_type = 'CUDA'
      # This is set by global settings on Slave, but might be overriden in Slave panel
      # bpy.context.user_preferences.system.compute_device = 'CUDA_MULTI_2'
   else:
      print('Slave keeping device for Cycles from Client: ' + bpy.context.scene.cycles.device)

# This can be overriden in Slave panel
# If not overriden, we use Client settings
if in_save_override_tile_active:
   print('Slave overriding tiles from ' + str(bpy.context.scene.render.tile_x) + 'x' + str(bpy.context.scene.render.tile_y) + ' to ' + str(in_save_override_tile_tile_x) + 'x' + str(in_save_override_tile_tile_y)) 
   bpy.context.scene.render.tile_x = in_save_override_tile_tile_x
   bpy.context.scene.render.tile_y = in_save_override_tile_tile_y
   if in_render_engine == 'CYCLES':
      bpy.context.scene.cycles.tile_order = in_save_override_tile_tile_order
else:
   print('Slave keeping tiles from Client ' + str(bpy.context.scene.render.tile_x) + 'x' + str(bpy.context.scene.render.tile_y)) 

# Set the thread count (specified in Slave panel)
bpy.context.scene.render.threads = in_thread_count;

# Set output path (should use Scene)
bpy.context.scene.render.filepath = in_save_path

# Set to use file extension
bpy.context.scene.render.use_file_extension = True

# Set file format
bpy.context.scene.render.image_settings.file_format = in_save_file_format

# TODO: Other settings that depend on Slave device (hardware spec),
# and affect rendering effectivity
# but do not affect rendering result (in theory) could be overriden in Slave panel

frame_idx = frame_idx_begin
while frame_idx < len(argv):
   print('Slave rendering frame no: ' + str(argv[frame_idx]) )
   # Set current frame
   bpy.context.scene.frame_set(int(argv[frame_idx]))
   # Set file path
   bpy.context.scene.render.filepath =  in_save_path + str(argv[frame_idx]).zfill(6) + str(bpy.context.scene.render.file_extension)
   # Do the rendering
   bpy.ops.render.render(write_still=True) # render still, animation=True
   # Go to next frame
   frame_idx += 1

