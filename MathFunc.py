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
from bpy.types import Operator, PropertyGroup, OperatorFileListElement
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, IntProperty, EnumProperty
import numpy as np
#import scipy.special as sp
from numpy import cos, sin, exp, log, sqrt, pi
from . import FunctionList

def create_faces_xyz(grid, faces):
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

def add_modifiers(mymesh, myobject, t):

    bpy.context.view_layer.objects.active = myobject
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.remove_doubles() 
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.select_mode( type  = 'FACE'   )
    bpy.ops.mesh.select_all( action = 'SELECT' )
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = t
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 3
    for f in mymesh.polygons:
        f.use_smooth = True

def create_faces(grid, faces):
    count = 0
    for k in range (0, (grid)*(grid-1)):
        if count < grid-1:
            A = k
            B = k+1
            C = k+(grid)+1
            D = k+(grid)
     
            face = (A,B,C,D)
            faces.append(face)
     
            count = count + 1
        else:
            count = 0

    return(faces)

def add_xyz_object(self, context):
    verts = []
    edges = []
    t_inc = self.theta_ubound/self.grid_size
    p_inc = self.phi_ubound/self.grid_size

    if self.default_input == 'TORUS':
        (x_input,y_input,z_input) = FunctionList.torus()
    elif self.default_input == 'SPHERE':
        (x_input,y_input,z_input) = FunctionList.sphere()
    elif self.default_input == 'DNA':
        (x_input,y_input,z_input) = FunctionList.dna()
    elif self.default_input == 'CURVES':
        (x_input,y_input,z_input) = FunctionList.curves()
    elif self.default_input == 'KLEINBOTTLE':
        (x_input,y_input,z_input) = FunctionList.kleinbot()
    elif self.default_input == 'KLEIN8':
        (x_input,y_input,z_input) = FunctionList.klein8()
    elif self.default_input == 'SHELL':
        (x_input,y_input,z_input) = FunctionList.shell()
    elif self.default_input == 'CYLINDER':
        (x_input,y_input,z_input) = FunctionList.cylinder()
    elif self.default_input == 'USER INPUT':  
	    (x_input,y_input,z_input) = (self.x_input, self.y_input, self.z_input)
   
    t = 0
    for i in range (0, self.grid_size + 1):
        p = 0
        for j in range(0, self.grid_size + 1):
            x = eval('%s' %x_input)
            y = eval('%s' %y_input)
            z = eval('%s' %z_input)
            vert = (x,y,z) 
            verts.append(vert)
            p = p + p_inc
        t = t + t_inc 

    mymesh = bpy.data.meshes.new("XYZ Function")
    myobject = bpy.data.objects.new("XYZ Function", mymesh)

    myobject.location = bpy.context.scene.cursor.location
    bpy.context.scene.collection.objects.link(myobject)
     
    mymesh.from_pydata(verts, edges, create_faces_xyz(self.grid_size, []))
    mymesh.update(calc_edges=True)

    add_modifiers(mymesh, myobject, 0.01)

def add_z_object(self, context):
    verts = []
    edges = []
    area = self.grid_size*self.grid_size
    sx = np.linspace(-self.x_bound,self.x_bound,self.grid_size)
    sy = np.linspace(-self.y_bound,self.y_bound,self.grid_size)
    x,y = np.meshgrid(sx, sy)

    if self.default_input == 'SADDLE':
        function = eval('%s' %FunctionList.saddle())
    elif self.default_input == 'TRIGONOMETRIC':
        function = eval('%s' %FunctionList.trigonometric())
    elif self.default_input == 'WAVE':
        function = eval('%s' %FunctionList.wave())
    elif self.default_input == 'EXPONENTIAL':
        function = eval('%s' %FunctionList.exponential())
    elif self.default_input == 'PYRAMID':
        function = eval('%s' %FunctionList.pyramid())
    elif self.default_input == 'PAPER':
        function = eval('%s' %FunctionList.paper())
    elif self.default_input == 'USER INPUT':  
	    function = eval('%s' %self.function_input)

    for i in range(len(x)):
        for j in range(len(x)):
                vert = (x[i][j],y[i][j],self.scaling_factor*function[i][j]) 
                verts.append(vert)
        
    mymesh = bpy.data.meshes.new("z Function")
    myobject = bpy.data.objects.new("z Function",mymesh)

    myobject.location = bpy.context.scene.cursor.location
    bpy.context.scene.collection.objects.link(myobject)

    mymesh.from_pydata(verts, edges, create_faces(self.grid_size, []))
    mymesh.update(calc_edges=True)

    add_modifiers(mymesh, myobject,	self.thickness)

def add_orbital_object(self, context):
    verts = []
    edges = []
    l = self.l 
    m = self.m 
    area = self.grid_size*self.grid_size 
    PHI, THETA = np.mgrid[0:2*np.pi:self.grid_size*1j, 0:np.pi:self.grid_size*1j]
    
    if self.representation_input == 'REAL':
        
        R = sp.sph_harm(self.m , self.l , PHI, THETA).real
        x = self.scaling_factor*R*sin(THETA)*cos(PHI)
        y = self.scaling_factor*R*sin(THETA)*sin(PHI)
        z = self.scaling_factor*R*cos(THETA)
        
        for i in range(len(x)):
            for j in range(len(x)):
                vert = (x[i][j],y[i][j],z[i][j]) 
                verts.append(vert)
    
    elif self.representation_input == 'IMAGINARY':
        
        R = sp.sph_harm(self.m , self.l , PHI, THETA).imag
        x = self.scaling_factor*R*sin(THETA)*cos(PHI)
        y = self.scaling_factor*R*sin(THETA)*sin(PHI)
        z = self.scaling_factor*R*cos(THETA)
        
        for i in range(len(x)):
            for j in range(len(x)):
                vert = (x[i][j],y[i][j],z[i][j]) 
                verts.append(vert)
            
    elif self.representation_input == 'ABSOLUTE':
        
        R = np.abs(sp.sph_harm(self.m , self.l , PHI, THETA))
        x = self.scaling_factor*R*sin(THETA)*cos(PHI)
        y = self.scaling_factor*R*sin(THETA)*sin(PHI)
        z = self.scaling_factor*R*cos(THETA)
        
        for i in range(len(x)):
            for j in range(len(x)):
                vert = (x[i][j],y[i][j],z[i][j]) 
                verts.append(vert)
            
    elif self.representation_input == "FIELD":
        R = sp.sph_harm(self.m , self.l , PHI, THETA).real
        s = 1
        x = self.scaling_factor*(s*R+0.5)*np.sin(THETA)*np.cos(PHI)
        y = self.scaling_factor*(s*R+0.5)*np.sin(THETA)*np.sin(PHI)
        z = self.scaling_factor*(s*R+0.5)*np.cos(THETA)
        
        for i in range(len(x)):
            for j in range(len(x)):
                vert = (x[i][j],y[i][j],z[i][j]) 
                verts.append(vert) 

    mymesh = bpy.data.meshes.new("Orbital")
    myobject = bpy.data.objects.new("Orbital",mymesh)

    myobject.location = bpy.context.scene.cursor.location
    bpy.context.scene.collection.objects.link(myobject)

    mymesh.from_pydata(verts, edges, create_faces(self.grid_size, []))
    mymesh.update(calc_edges=True)

    add_modifiers(mymesh, myobject, self.thickness)

class xyz_OT_add_object(Operator):
    bl_idname = "mesh.add_xyz"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    Funcs = [
        ("TORUS", "Torus", "", 1),
        ("SPHERE", "Sphere", "", 2),
        ("DNA", "Dna", "", 3),
        ("CURVES", "Curves", "", 4),
        ("KLEINBOTTLE", "Klein Bottle", "", 5),
        ("KLEIN8", "Klein8", "", 6),
        ("SHELL", "Shell", "", 7),
        ("CYLINDER", "Cylinder", "", 8),
        ("USER INPUT", "User Input", "", 9),
	]

    default_input = EnumProperty(
        items = Funcs,
        name = "Default Functions"
    )

    x_input: StringProperty(
        name="X",
        default = ''
    )
    
    y_input: StringProperty(
        name="Y",
        default = ''
    )
    
    z_input: StringProperty(
        name="Z",
        default = ''
    )

    theta_ubound: FloatProperty(
        name="Theta Upper Bound",
        default = 2*pi,
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
    
    def execute(self, context):

        add_xyz_object(self, context)

        return {'FINISHED'}

class z_OT_add_object(Operator):
    bl_idname = "mesh.add_z"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    Func = [
        ("SADDLE", "Saddle", "", 1),
        ("TRIGONOMETRIC", "Trigonometric", "", 2),
        ("WAVE", "Wave", "", 3),
        ("EXPONENTIAL", "Exponential", "", 4),
        ("PYRAMID", "Pyramid", "", 5),
        ("PAPER", "Paper", "", 6),
        ("USER INPUT", "User input", "", 7),
    ]

    default_input = EnumProperty(
        items = Func,
        name = "Default Functions"
    )

    function_input: StringProperty(
        name = 'Function',
        default = ''
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

def register():
    bpy.utils.register_class(xyz_OT_add_object)
    bpy.utils.register_class(z_OT_add_object)
    bpy.utils.register_class(orbital_OT_add_object)
    bpy.types.VIEW3D_MT_mesh_add.append(add_xyz_button)
    bpy.types.VIEW3D_MT_mesh_add.append(add_z_button)   
    bpy.types.VIEW3D_MT_mesh_add.append(add_orbital_button)

def unregister():
	bpy.utils.unregister_class(xyz_OT_add_object)
	bpy.utils.unregister_class(z_OT_add_object)
	bpy.utils.unregister_class(orbital_OT_add_object)
	bpy.types.VIEW3D_MT_mesh_add.remove(add_xyz_button)
	bpy.types.VIEW3D_MT_mesh_add.remove(add_z_button)   
	bpy.types.VIEW3D_MT_mesh_add.remove(add_orbital_button)
