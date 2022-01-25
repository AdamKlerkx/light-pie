import bpy
from bpy.types import Menu

type = False
empty_x = 0
empty_y = 0
empty_z = 0
loc_empty_x = 0
loc_empty_y = 0
loc_empty_z = 0


bl_info = {
    "name": "lightpie",
    "author": "Adam Klerkx",
    "version": (0, 0, 1, 5),
    "description": "an addon that gives you quick lighting setups sised correctly around your model.",
    "blender": (2, 90, 0),
    "category": "3D view"
}

def cube_to_empty():
    x, y, z = bpy.context.active_object.scale
    empty_x, empty_y, empty_z = bpy.context.active_object.dimensions
    loc_empty_x, loc_empty_y, loc_empty_z = bpy.context.active_object.location
    
    bpy.ops.object.delete(use_global=False)
    bpy.ops.object.empty_add(type='CUBE', align='WORLD', location=(loc_empty_x, loc_empty_y, loc_empty_z), scale=(1, 1, 1))
    bpy.ops.transform.resize(value=(x, y, z))
    return empty_x, empty_y, empty_z, loc_empty_x, loc_empty_y, loc_empty_z

def Z(input):
    
    strength = 100
    loc_z = 2+2*empty_z+loc_empty_z
    strength = 100+empty_z*input
        
    return loc_z, strength
    
def basic_light():
    
    loc_z, strength = Z(3)

    if empty_x < 0.5:
        loc_x = empty_x + 2.5
    else:
        loc_x = empty_x*3
    
    if empty_y < 0.5:
        loc_y = empty_y + 2.5
    else:
        loc_y = empty_y*3
    
        
    bpy.ops.object.light_add(type='AREA', radius=1, align='WORLD', location=(loc_empty_x, loc_empty_y, loc_z + loc_empty_z))
    bpy.ops.transform.resize(value=(loc_x, loc_y, 1))
    bpy.context.active_object.data.energy = strength

def window_light():
    
    loc_z, strength = Z(5)
        
    if empty_x != empty_y or empty_y != empty_x:
        if empty_x > empty_y:
            loc_x = empty_x / 2
            loc_y = empty_x / 2
            rad = empty_x / 1.15
        if empty_y > empty_x:
            loc_y = empty_y / 2
            loc_x = empty_y / 2
            rad = empty_y / 1.15
    else:
        loc_x = empty_x / 2
        loc_y = empty_y / 2
        rad = empty_x / 1.15

    bpy.ops.object.light_add(type='AREA', radius=rad, align='WORLD', location=(loc_empty_x + loc_x, loc_empty_y + loc_y, 0))
    bpy.ops.transform.translate(value=(0, 0, loc_z))
    bpy.context.active_object.data.energy = strength
    bpy.ops.object.light_add(type='AREA', radius=rad, align='WORLD', location=(loc_empty_x + loc_x, loc_empty_y - loc_y, 0))
    bpy.ops.transform.translate(value=(0, 0, loc_z))
    bpy.context.active_object.data.energy = strength
    bpy.ops.object.light_add(type='AREA', radius=rad, align='WORLD', location=(loc_empty_x - loc_x, loc_empty_y + loc_y, 0))
    bpy.ops.transform.translate(value=(0, 0, loc_z))
    bpy.context.active_object.data.energy = strength
    bpy.ops.object.light_add(type='AREA', radius=rad, align='WORLD', location=(loc_empty_x - loc_x, loc_empty_y - loc_y, 0))
    bpy.ops.transform.translate(value=(0, 0, loc_z))
    bpy.context.active_object.data.energy = strength


class MESH_OT_setup_cube(bpy.types.Operator):
    """cube setup"""
    bl_idname = "mesh.setup_cube"
    bl_label = "setup cube"

    
    def execute(self, context):
        global empty_x, empty_y, empty_z, loc_empty_x, loc_empty_y, loc_empty_z
        empty_x, empty_y, empty_z, loc_empty_x, loc_empty_y, loc_empty_z = cube_to_empty()
        type = True
        panel(type)
        
        return {'FINISHED'}

class MESH_OT_setup_cube_pie(bpy.types.Operator):
    """cube setup"""
    bl_idname = "mesh.setup_cube_pie"
    bl_label = "setup cube pie"

    
    def execute(self, context):
        global empty_x, empty_y, empty_z, loc_empty_x, loc_empty_y, loc_empty_z
        empty_x, empty_y, empty_z, loc_empty_x, loc_empty_y, loc_empty_z = cube_to_empty()
        bpy.ops.wm.call_menu_pie(name="light_pie")
        type = True
        
        return {'FINISHED'}

class MESH_OT_basic_light(bpy.types.Operator):
    """lol"""
    bl_idname = "mesh.basic_light"
    bl_label = "basic light"
    
    def execute(self, context):
        basic_light()
        return {'FINISHED'}

class MESH_OT_window_light(bpy.types.Operator):
    """lol"""
    bl_idname = "mesh.window_light"
    bl_label = "window light"
    
    def execute(self, context):
        window_light()
        return {'FINISHED'}


class light_pie(Menu):
    bl_label = "Select Lighting setup"
    

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        
        pie.operator("mesh.window_light")
        pie.operator("mesh.basic_light")
        pie.operator("mesh.ei")

addon_keymaps = []

def panel(type):
    if type == True:
        bpy.utils.register_class(light_panel_full)
        type == False


class light_panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "lighting"
    bl_idname = "SCENE_PT_test"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'lightpie'

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.label(text="setup cube:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("mesh.setup_cube")
        

class light_panel_full(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "lighting"
    bl_idname = "SCENE_PT_test"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'lightpie'

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.label(text="setup cube:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("mesh.setup_cube")
        
        layout.label(text="light setups:")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("mesh.basic_light")
        row = layout.row(align=True)
        row.operator("mesh.window_light")
        row = layout.row(align=True)

def register():
    bpy.utils.register_class(MESH_OT_basic_light)
    bpy.utils.register_class(MESH_OT_window_light)
    bpy.utils.register_class(light_pie)
    bpy.utils.register_class(MESH_OT_setup_cube)
    bpy.utils.register_class(MESH_OT_setup_cube_pie)
    bpy.utils.register_class(light_panel)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new("mesh.setup_cube_pie", type ='F', value='PRESS', shift = True)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_item.remove(kmi)
    addon_keymaps.clear()
            
    bpy.utils.unregister_class(MESH_OT_basic_light)
    bpy.utils.unregister_class(MESH_OT_window_light)
    bpy.utils.unregister_class(light_pie)
    bpy.utils.unregister_class(MESH_OT_setup_cube)
    bpy.utils.unregister_class(MESH_OT_setup_cube_pie)
    bpy.utils.unregister_class(light_panel)
    bpy.utils.unregister_class(light_panel_full)


if __name__ == "__main__":
    register()

bpy.ops.wm.call_menu_pie(name="light_panel")
