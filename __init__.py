bl_info = {
    "name": "Math Functions",
    "author": "Julian Melendez",
    "version": (1, 2),
    "blender": (2, 93, 3),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

import bpy

from . import MathFunc

def register():
	MathFunc.register()

def unregister():
    MathFunc.unregister()

if __name__ == "__main__":
    register()



