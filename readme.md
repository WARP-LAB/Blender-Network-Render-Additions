Blender Network Render Additions
============================

---

## About

The intention of this fork is to add functionality to Blender Network Render.

*The intention is not to replace renderfarms with jobs systems and such, rather it is designed to interactively render a single image over a network with immediate feedback in Blender. This requires a quite different design than render farms, although in certain simple cases it could serve as a replacement.*

Network Renderer (packed together with stable releases) by Martin Poirier <http://wiki.blender.org/index.php/Dev:2.6/Source/Render/Cycles/Network_Render>

Fork of this addon is pulled out from addon state in Blender 2.75a stable

---

## Fork additions

![Slave panel](https://raw.githubusercontent.com/WARP-LAB/Blender-Network-Render-Additions/master/readme/screen-01.jpg)

### Slave overrides - Compute device and Tiles size


It is Slave who should define the preferred rendering device as each Slave has different hardware capabilities (GPU/CPU).
This makes rendering effective in terms of speed, but does not affect rendering result in terms of image (scene can be rendered mixing GPU and CPU capable Slaves).

Slave can (should) override

* Enable/disable compute device override on Slave (Cycles Render)
  * Specify compute device (Cycles Render)
  

* Enable/disable tile size override on Slave (Cycles Render, Blender Internal Render)
  * Specify tile order (Cycles Render)
  * Specify tile size X (Cycles Render, Blender Internal Render)
  * Specify tile size Y (Cycles Render, Blender Internal Render)


The tile size override is present, as tile sizes should correspond to compute device type. Basically, always when Slave overrides compute device (thus renderer is Cycles) also size for tiles should be overridden. Rule of thumb - GPU 256x256, CPU 16x16. Read more [here](http://adaptivesamples.com/2013/11/05/auto-tile-size-addon-updated-again/) and [any other article](https://www.google.com/search?rls=en&q=speeding+up+blender+cycles&ie=UTF-8&oe=UTF-8) that discusses speeding up cycles.

*Before this addition Slave rendered the file with settings as they are set on Client. Client that doesn't have GPU capabilities can't specify that Slaves should render on GPU as there is no device dropdown (i.e., jobs sent from Mac with ATI card rendered on GPU-ready Slaves using CPU). And then there is issue with Client that had GPU capabilities (and file is set accordingly) working together with Slave that has only CPU support. Corresponding ticket <https://developer.blender.org/T46071>*

### Master - Slave timeout

Master can specify timeout (in minutes) after which master considers Slave dead if a frame from Slave hasn't been received. N.B., this is timeout for frame, not for the whole animation time.

*Previously this was hardcoded and Master considered any Slave executing job (frame on Slave) more than 5 minutes as dead, cancelled the job, resulting in socket timeout on Slave and finally crashing exception. Thus it was not possible to create über high quality final renderings not to mention "render me one image for the the whole weekend" tasks.*

---

## Install

Replace directory `netrender` in your Blender `addons` directory with `netrender` directory found in this repo. Restart Blender.


##### GNU/Linux  
`<Blender Installation Directory>/2.75/scripts/addons`

##### OSX  
`<Blender Installation Directory>/Blender.app/Contents/Resources/2.75/scripts/addons`

##### MSW  
`<Blender Installation Directory>\2.75\scripts\addons`

---

## Status

##### Done  
* Rendering (stills and animation) implemented and tested (*Render on slave*) on all OSes.

##### Todo  
* Overrides for baking shouldn't work as no line of code is written for it yet.
* Overrides for thumbnail generation shouldn't work as no line of code is written for it yet.

---

## License

Original author Martin Poirier

Contrubutions by kroko / Reinis Adovics (WARP)


```
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


```

