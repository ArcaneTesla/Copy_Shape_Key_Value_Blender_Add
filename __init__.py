bl_info = {
    "name": "Copy Shape Key Value",
    "author": "ArcaneTesla",
    "version": (0, 9),
    "blender": (3, 4, 0),
    "location": "View3D > UI > CopyShapeKeyValue",
    "description": "A small addon to speed up work with the same Shape Key on different models.",
    "warning": "This addon does not copy shape keys, only their values! If you find bugs, please report them.",
    "doc_url": "https://github.com/ArcaneTesla/Copy-Shape-Key-Value-Blender-Add/blob/develop/README.md",
    "tracker_url": "https://github.com/ArcaneTesla/Copy-Shape-Key-Value-Blender-Add/issues",
    "category": "Object",
}

import bpy

class CSKVPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Copy Shape Key Value"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CopyShapeKeyValue'

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.label(text="Source: ")
        row = layout.row()
        row.prop_search(scene, "selected_source_object", scene, "objects", text="")
        
        layout.label(text="Optional settings: ")
        
        layout.prop(scene, "all_checkbox", toggle=False, text="All shape key")
        
        row = layout.row()
        row.enabled = not scene.all_checkbox
        
        if scene.selected_source_object and scene.selected_source_object.data:
            row.prop_search(scene, "selected_source_shape_key", scene.selected_source_object.data.shape_keys, "key_blocks", text="")
        
        layout.prop(scene, "extra_value", slider=True)
    
        layout.label(text="Copy shape key value to: ")
        row = layout.row()
        row.prop_search(scene, "selected_target_object", scene, "objects", text="")
        
        row = layout.row()
        row.operator("object.copy_shape_key_value", text="Copy")
        
        
class CopyShapeKeyOperatorValue(bpy.types.Operator):
    bl_idname = "object.copy_shape_key_value"
    bl_label = "Copy Shape Key Value"

    def execute(self, context):
        
        value = context.scene.extra_value
        scene = context.scene
        obj = context.object
        
        source_obj = scene.selected_source_object
        target_obj = scene.selected_target_object
        
        
        if (source_obj and target_obj):
            source_shape_keys = source_obj.data.shape_keys
            target_shape_keys = target_obj.data.shape_keys
            if obj.show_only_shape_key == True:
                obj.show_only_shape_key = False
                self.report({'INFO'}, "Key Lock off ")

        else:
            self.report({'ERROR'}, "Please select both source and target objects")
            return {'CANCELLED'}   
        
                 
        if scene.all_checkbox == False and scene.selected_source_shape_key == "":
            self.report({'ERROR'}, "You have not selected any shape keys")
            return {'CANCELLED'}
           
        elif source_shape_keys is None or target_shape_keys is None:
            self.report({'ERROR'}, "Both objects must have shape keys")
            return {'CANCELLED'}     
        
        else:       
            check = True
            if scene.all_checkbox:
                for source_key_block in source_shape_keys.key_blocks:
                    for target_key_block in target_shape_keys.key_blocks:                  
                            if source_key_block.name == target_key_block.name:
                                target_key_block.value = source_key_block.value + value
                                check = False
            else:
                for target_key_block in target_shape_keys.key_blocks:
                    if target_key_block.name == scene.selected_source_shape_key:
                        source_key_block = source_shape_keys.key_blocks[scene.selected_source_shape_key]
                        target_key_block.value = source_key_block.value + value
                        check = False
                        break
        
        if check:
            self.report({'ERROR'}, "Shape keys with same names not found in target object")
            return {'CANCELLED'}
        
        self.report({'INFO'}, "Copy successful!")

        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(CSKVPanel)
    bpy.utils.register_class(CopyShapeKeyOperatorValue)
    bpy.types.Scene.selected_source_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.selected_target_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.extra_value = bpy.props.FloatProperty(name="Extra value", min=0, max=1, default=0.00000)
    bpy.types.Scene.all_checkbox = bpy.props.BoolProperty(name="All_checkbox", default=True)
    bpy.types.Scene.selected_source_shape_key = bpy.props.StringProperty(name="Selected source shape key")

def unregister():
    del bpy.types.Scene.selected_source_shape_key
    del bpy.types.Scene.all_checkbox
    del bpy.types.Scene.extra_value
    del bpy.types.Scene.selected_source_object
    del bpy.types.Scene.selected_target_object
    bpy.utils.unregister_class(CopyShapeKeyOperatorValue)
    bpy.utils.unregister_class(CSKVPanel)
    
if __name__ == "__main__":
    register()