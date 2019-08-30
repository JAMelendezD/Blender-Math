bl_info = {
    "name": "Math Functions",
    "author": "Julian Melendez",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, IntProperty, EnumProperty
from bpy_extras.object_utils import object_data_add
from mathutils import Vector
import numpy as np
import scipy.special as sp
from numpy import cos, sin, exp, log, sqrt, pi


def create_faces(grid, faces):
    count = 0
    for i in range (0, (grid + 1) *(grid)):
        if count < grid:
            A = i
            B = i+1
            C = (i+(grid+1))+1
            D = (i+(grid+1))
     
            face = (A,B,C,D)
            faces.append(face)
     
            count = count + 1
        else:
            count = 0

    return(faces)

def add_xyz_object(self, context):
    # mesh arrays
    verts = []
    faces = []
    edges = []
     
    factor = self.scaling_factor
    grid = self.grid_size
     
    t_inc = self.theta_ubound/grid
    p_inc = self.phi_ubound/grid
     
    #fill verts array
    t = self.theta_lbound
    for i in range (0, grid + 1):
        p = self.phi_lbound
        for j in range(0,grid + 1):
            x = factor*eval('%s' %self.x_input)
            y = factor*eval('%s' %self.y_input)
            z = factor*eval('%s' %self.z_input)
     
            vert = (x,y,z) 
            verts.append(vert)
            #increment phi
            p = p + p_inc
        #increment theta
        t = t + t_inc
    
    create_faces(grid, faces)
            
    #create mesh and object
    mymesh = bpy.data.meshes.new("XYZ Function")
    myobject = bpy.data.objects.new("XYZ Function",mymesh)
     
    #set mesh location
    myobject.location = bpy.context.scene.cursor.location
    bpy.context.scene.collection.objects.link(myobject)
     
    #create mesh from python data
    mymesh.from_pydata(verts,edges,faces)
    mymesh.update(calc_edges=True)
     
    #set the object to edit mode
    bpy.context.view_layer.objects.active = myobject
    bpy.ops.object.mode_set(mode='EDIT')
     
    # remove duplicate vertices
    bpy.ops.mesh.remove_doubles() 
    bpy.ops.mesh.normals_make_consistent(inside=False)


    bpy.ops.mesh.select_mode( type  = 'FACE'   )
    bpy.ops.mesh.select_all( action = 'SELECT' )

    bpy.ops.mesh.flip_normals()

    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = self.thickness

    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 3

    #smooth shading
    for f in mymesh.polygons:
        f.use_smooth = True

def add_z_object(self, context):
    verts = []
    faces = []
    edges = []
     
    #fill verts array
    grid = self.grid_size
    factor = self.scaling_factor
    xb = self.x_bound
    yb = self.y_bound

    area = grid*grid
    sx = np.linspace(-xb,xb,grid)
    sy = np.linspace(-yb,yb,grid)
    x,y = np.meshgrid(sx, sy)
    function = eval('%s' %self.function_input)

    for i in range(len(x)):
        for j in range(len(x)):
                vert = (x[i][j],y[i][j],factor*function[i][j]) 
                verts.append(vert)

    create_faces(grid, faces)
       
    #create mesh and object
    mymesh = bpy.data.meshes.new("z Function")
    myobject = bpy.data.objects.new("z Function",mymesh)

    #set mesh location
    myobject.location = bpy.context.scene.cursor.location
    bpy.context.scene.collection.objects.link(myobject)

    #create mesh from python data
    mymesh.from_pydata(verts,edges,faces)
    mymesh.update(calc_edges=True)

    #set the object to edit mode
    bpy.context.view_layer.objects.active = myobject
    bpy.ops.object.mode_set(mode='EDIT')
     
    # remove duplicate vertices
    bpy.ops.mesh.remove_doubles() 
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = self.thickness

    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 3

    #smooth shading
    for f in mymesh.polygons:
        f.use_smooth = True


def add_orbital_object(self, context):
    verts = []
    faces = []
    edges = []

    factor = self.scaling_factor
    plot = self.representation_input
    l = self.l 
    m = self.m 
    grid = self.grid_size
    area = grid*grid   
    PHI, THETA = np.mgrid[0:2*np.pi:grid*1j, 0:np.pi:grid*1j]
    
    if plot == 'REAL':
        
        R = sp.sph_harm(m, l, PHI, THETA).real
        x = factor*R*sin(THETA)*cos(PHI)
        y = factor*R*sin(THETA)*sin(PHI)
        z = factor*R*cos(THETA)
        
        for i in range(len(x)):
            for j in range(len(x)):
                vert = (x[i][j],y[i][j],z[i][j]) 
                verts.append(vert)
    
    elif plot == 'IMAGINARY':
        
        R = sp.sph_harm(m, l, PHI, THETA).imag
        x = factor*R*sin(THETA)*cos(PHI)
        y = factor*R*sin(THETA)*sin(PHI)
        z = factor*R*cos(THETA)
        
        for i in range(len(x)):
            for j in range(len(x)):
                vert = (x[i][j],y[i][j],z[i][j]) 
                verts.append(vert)
            
    elif plot == 'ABSOLUTE':
        
        R = np.abs(sp.sph_harm(m, l, PHI, THETA))
        x = factor*R*sin(THETA)*cos(PHI)
        y = factor*R*sin(THETA)*sin(PHI)
        z = factor*R*cos(THETA)
        
        for i in range(len(x)):
            for j in range(len(x)):
                vert = (x[i][j],y[i][j],z[i][j]) 
                verts.append(vert)
            
    elif plot == "FIELD":
        R = sp.sph_harm(m, l, PHI, THETA).real
        s = 1
        x = factor*(s*R+1)*np.sin(THETA)*np.cos(PHI)
        y = factor*(s*R+1)*np.sin(THETA)*np.sin(PHI)
        z = factor*(s*R+1)*np.cos(THETA)
        
        for i in range(len(x)):
            for j in range(len(x)):
                vert = (x[i][j],y[i][j],z[i][j]) 
                verts.append(vert)
    
    create_faces(grid, faces)

    #create mesh and object
    mymesh = bpy.data.meshes.new("Orbital")
    myobject = bpy.data.objects.new("Orbital",mymesh)

    #set mesh location
    myobject.location = bpy.context.scene.cursor.location
    bpy.context.scene.collection.objects.link(myobject)

    #create mesh from python data
    mymesh.from_pydata(verts,edges,faces)
    mymesh.update(calc_edges=True)

    #set the object to edit mode
    bpy.context.view_layer.objects.active = myobject
    bpy.ops.object.mode_set(mode='EDIT')
     
    # remove duplicate vertices
    bpy.ops.mesh.remove_doubles() 
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = self.thickness

    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 3

    #smooth shading
    for f in mymesh.polygons:
        f.use_smooth = True


class xyz_OT_add_object(Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_xyz"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}
        
    x_input: StringProperty(
        name="X",
        default = "(2+cos(p))*cos(t)"
    )
    
    y_input: StringProperty(
        name="Y",
        default = "(2+cos(p))*sin(t)"
    )
    
    z_input: StringProperty(
        name="Z",
        default = "sin(p)"
    )
    
    theta_lbound: FloatProperty(
        name="Theta Lower Bound",
        default = 0,
        step = (pi/4)*100
    )
    
    theta_ubound: FloatProperty(
        name="Theta Upper Bound",
        default = 2*pi,
        step = (pi/4)*100
    )

    
    phi_lbound: FloatProperty(
        name="Phi Lower Bound",
        default = 0,
        step = (pi/4)*100
    )
    
    phi_ubound: FloatProperty(
        name="Phi Upper Bound",
        default = 2*pi,
        step = (pi/4)*100
    )
    
    
    grid_size: IntProperty(
        name="Grid Subdivisions",
        default = 10,
        min = 10,
        max = 100
    )
    
    scaling_factor: FloatProperty(
        name="Scale",
        default = 1.0
    )
    
    thickness: FloatProperty(
        name="Thickness",
        default = 0.1
    )

    
    def execute(self, context):

        add_xyz_object(self, context)

        return {'FINISHED'}


class z_OT_add_object(Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_z"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}
        
    function_input: StringProperty(
        name="Function",
        default = "x**2-y**2"
    )
    
    grid_size: IntProperty(
        name="Grid Subdivisions",
        default = 20,
        min = 10,
        max = 100
    )
    
    x_bound: FloatProperty(
        name="X Size",
        default = -1.0
    )
    
    y_bound: FloatProperty(
        name="Y Size",
        default = 1.0
    )
    
    scaling_factor: FloatProperty(
        name="Scale",
        default = 1.0
    )
    
    thickness: FloatProperty(
        name="Thickness",
        default = 0.1
    )

    
    def execute(self, context):

        add_z_object(self, context)

        return {'FINISHED'}


class orbital_OT_add_object(Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_orbital"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    Rep = [
        ("REAL", "Real", "", 1),
        ("IMAGINARY", "Imaginary", "", 2),
        ("ABSOLUTE", "Absolute", "", 3),
        ("FIELD", "Field", "", 4),
    ]
    
    representation_input = EnumProperty(
        items = Rep,
        name = "Representation"
    )
    
        
    l: IntProperty(
        name="l",
        default = 0,
        min = 0,
        max = 10
    )
    
    m: IntProperty(
        name="m",
        default = 0,
        min = -10,
        max = 10
    )
    
    
    grid_size: IntProperty(
        name="Grid Subdivisions",
        default = 20,
        min = 10,
        max = 100
    )
    
    scaling_factor: FloatProperty(
        name="Scale",
        default = 1.0
    )
    
    thickness: FloatProperty(
        name="Thickness",
        default = 0.1
    )

    
    def execute(self, context):

        add_orbital_object(self, context)

        return {'FINISHED'}


# Registration

def add_xyz_button(self, context):
    self.layout.operator(
        xyz_OT_add_object.bl_idname,
        text="XYZ",
        icon='PLUGIN')

def add_z_button(self, context):
    self.layout.operator(
        z_OT_add_object.bl_idname,
        text="Z Function",
        icon='PLUGIN')

def add_orbital_button(self, context):
    self.layout.operator(
        orbital_OT_add_object.bl_idname,
        text="Orbitals",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(xyz_OT_add_object)
    bpy.utils.register_class(z_OT_add_object)
    bpy.utils.register_class(orbital_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_xyz_button)
    bpy.types.VIEW3D_MT_mesh_add.append(add_z_button)   
    bpy.types.VIEW3D_MT_mesh_add.append(add_orbital_button)


def unregister():
    bpy.utils.unregister_class(xyz_OT_add_object)
    bpy.utils.unregister_class(z_OT_add_object)
    bpy.utils.unregister_class(orbital_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_xyz_button)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_z_button)   
    bpy.types.VIEW3D_MT_mesh_add.remove(add_orbital_button)
