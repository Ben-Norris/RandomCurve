# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Random Curve",
    "author" : "Ben Norris",
    "description" : "Generates random curves",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Add Curve"
}

import bpy
from bpy.props import (IntProperty, FloatProperty, BoolProperty, StringProperty, PointerProperty)
from bpy.types import (Panel, Operator, PropertyGroup)
import random
from mathutils import Vector
from random import randint

#REMOVE
#number_of_verts = 25
#number_of_objects = 50
twist_rate = 4.0
xyz = ['X', 'Y', 'Z']
#make_3d = True
#exclude_axis = 'Z'
#axis = 'Z'
#bevel = True

#ui props
class RandomCurveProps(PropertyGroup):
    vert_num : IntProperty(name = "Number of Verts", description = "Number of verts per curve", default = 10, min = 0, max = 50, soft_max = 50)
    obj_num : IntProperty(name = "Number of Curves", description = "Number of curves to generate", default = 10, min = 1, max = 100, soft_max = 100)
    twist : FloatProperty(name = "Twist Rate", description = "Twisting of verts", default = 4.0, min = 0, max = 5, precision = 2)
    is3D : BoolProperty(name = "Make 3D", description = "Should curves be created in all 3 axis", default = True)
    axis_to_exclude : StringProperty(name = "Exclude Axis", description = "This axis is not used during curve generation", default = 'Y')
    #_axis : StringProperty(name = "", description = "")
    enable_bevel : BoolProperty(name = "Bevel Curve", description = "Should curves be beveled", default = True)
    taper_object_name : StringProperty(name = "", description = "The taper object for the curves", default = '')
    bevel_object_name : StringProperty(name = "", description = "The bevel object for the curves", default = '')
    bevel_min : FloatProperty(name = "Min", description = "Minimum bevel value", default = 0.1, min = 0.1, max = 100, precision = 2)
    bevel_max : FloatProperty(name = "Max", description = "Maximum bevel value", default = 5.0, min = 0.1, max = 100, precision = 2)

#get a random number
def RandNum():
    return random.uniform(-twist_rate, twist_rate)

#excludes an axis from the extrusion
def Generate2D(exclude_axis):
    print('excluding ' + exclude_axis)

    if 'X' in exclude_axis:
        randVector = (0,RandNum(),RandNum())
    elif 'Y' in exclude_axis:
        randVector = (RandNum(),0,RandNum())
    elif 'Z' in exclude_axis:
        randVector = (RandNum(),RandNum(),0)
    
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":randVector})

#main extrusion used in operator
def Extrude():
    transform = bpy.ops.transform
    curve = bpy.ops.curve
    mesh = bpy.ops.mesh
    _object = bpy.ops.object
    #prop setup
    rc_props = bpy.context.scene.rcprop
    number_of_verts = rc_props.vert_num
    number_of_objects = rc_props.obj_num
    twist_rate = rc_props.twist
    make_3d = rc_props.is3D
    exclude_axis = rc_props.axis_to_exclude
    bevel = rc_props.enable_bevel
    bevel_min_value = rc_props.bevel_min
    bevel_max_value = rc_props.bevel_max 
    taper_object = rc_props.taper_object_name
    bevel_object = rc_props.bevel_object_name

    #creates a taper object if there is not one or uses taper object with name
    if bevel:

        if len(taper_object)>0:
            obj = bpy.data.objects[taper_object].select_set(True)
            _object.editmode_toggle()
            curve.select_all(action='SELECT')
            transform.translate(value=(0, 0.00198041, 0))
        elif len(taper_object)<1:
            curve.primitive_bezier_curve_add(radius=1, enter_editmode=True, location=(0, 0, 0))
            curve.select_all(action='SELECT')
            transform.translate(value=(0, 0.00198041, 0))
            bpy.context.active_object.name = 'TaperObject'
            taper_object = 'TaperObject'

        


    #create objects
    for t in range(number_of_objects):
        mesh.primitive_cube_add(enter_editmode=True, location=(0, 0, 0))
        mesh.select_all(action='SELECT')
        transform.resize(value=(0,0,0))
        mesh.remove_doubles()
        
        #extrude objects
        for i in range(number_of_verts):
            if not make_3d:
                Generate2D(exclude_axis)
            else: 
                rand_vector = (random.random(),random.random(),random.random())
                mesh.extrude_region_move(TRANSFORM_OT_translate={"value":rand_vector})
        
        #find random axis to rotate on
        if make_3d:
            value = randint(0, 2)
            if value == 0:
                axis = 'X'
            elif value == 1:
                axis = 'Y'
            else:
                axis = 'Z'
        else:
            axis = exclude_axis
            
        _object.editmode_toggle()

        #rotate objects
        if not make_3d:
            randRotate = random.uniform(-360, 360)
            transform.rotate(value=randRotate, orient_axis=axis)
        else:
            for i in range(3):
                randRotate = random.uniform(-360, 360)
                transform.rotate(value=randRotate, orient_axis=xyz[i])
        
        #convert to curve and beveling
        if bevel:
            _object.convert(target='CURVE')
            if len(bevel_object)>0:
                bpy.context.object.data.bevel_object = bpy.data.objects[bevel_object]
            bevelDepth = random.uniform(bevel_min_value, bevel_max_value)
            bpy.context.object.data.bevel_depth = bevelDepth
            bpy.context.object.data.taper_object = bpy.data.objects[taper_object]
            _object.subdivision_set(level=2, relative=False)
            _object.shade_smooth()

#operator
class Random_Curve_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.random_curve"
    bl_label = "Random Curve"
    bl_description = "Make random curves!"

    def execute(self, context):
        Extrude()
        return{'FINISHED'}

#ui
class Random_Curve_PT_Panel(bpy.types.Panel):
    bl_idname = "Random_Curve_PT_Panel"
    bl_label = "Random Curve"
    bl_category = "Random Curve"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=False)
        row = col.row(align=True)

        col.label(text="Generation Values")
        col.prop(scene.rcprop, "vert_num")
        col.prop(scene.rcprop, "obj_num")
        col.prop(scene.rcprop, "twist")


        col.separator()
        col.label(text="Rotation")
        col.prop(scene.rcprop, "is3D")
        col.prop(scene.rcprop, "axis_to_exclude")

        col.separator()
        col.label(text="Bevel Options")
        col.prop(scene.rcprop, "enable_bevel")
        bevel = scene.rcprop.enable_bevel
        if bevel == True:
            col.label(text="Taper Object Name")
            col.prop(scene.rcprop, "taper_object_name")
            col.label(text="Bevel Object Name")
            col.prop(scene.rcprop, "bevel_object_name")
            col.label(text="Random Bevel Depth")
            col.prop(scene.rcprop, "bevel_min")
            col.prop(scene.rcprop, "bevel_max")

        col.separator()
        col.label(text="Generate")
        col.operator('view3d.random_curve', text="Make Random Curves!")

#blender addon reg, unreg
def register():
    bpy.utils.register_class(Random_Curve_OT_Operator)
    bpy.utils.register_class(Random_Curve_PT_Panel)
    bpy.utils.register_class(RandomCurveProps)
    bpy.types.Scene.rcprop = PointerProperty(type=RandomCurveProps)

def unregister():
    bpy.utils.unregister_class(Random_Curve_OT_Operator)
    bpy.utils.unregister_class(Random_Curve_PT_Panel)
    bpy.utils.unregister_class(RandomCurveProps)
    del bpy.types.Scene.rcprop

if __name__ == "__main__":
    register()
