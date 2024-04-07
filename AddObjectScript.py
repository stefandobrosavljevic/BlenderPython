import bpy
bl_info = {
    "name": "My First Addon",  # name of the addon
    "author": "Stefan Dobrosavljevic",  # name of addon author
    "version": (1, 0),  # version of addon
    # minimum versoin of Blender that the addon is compatible
    "blender": (2, 80, 0),
    # description where in Blender's UI the addon can be found
    "location": "View3D > Tool",
    "description": "This is a sample addon for Blender",  # description what addon does
    "warning": "",  # warinng or important notes
    "wiki_url": "",
    # the category that the addon falls under in Blender’s addon list
    "category": "Add Mesh",
}


class TestPanel(bpy.types.Panel):
    bl_label = "Test Panel"  # display name of the class in UI
    bl_idname = "PT_TestPanel"  # unique identifier for the class
    bl_space_type = "VIEW_3D"  # sets space type where the class will be displayed
    # sets the region within the space type context where the class is to be displayed
    bl_region_type = "UI"
    # sets the tab category where the class will be located in UI
    bl_category = "My 1st Addon"
    bl_description = ""  # discription for the class
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Sample text", icon="CUBE")
        row = layout.row()
        row.operator("mesh.primitive_cube_add", icon="CUBE")
        row = layout.row()
        row.operator("mesh.primitive_uv_sphere_add", icon="SPHERE")

    def pool(self):  # optional method, when defined, determines whether the class can be used in the current context
        pass

    def execute():  # method is called when running the operator
        pass

    def invoke():  # this method is called to start interactive operators
        pass


class PanelA(bpy.types.Panel):
    bl_label = "Scaling"
    bl_idname = "PT_PanelA"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My 1st Addon"
    bl_parent_id = "PT_TestPanel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.label(text="This is Panel A", icon="STYLUS_PRESSURE")
        row = layout.row()
        row.operator("transform.resize")
        row = layout.row()

        col = layout.column()
        col.prop(obj, "scale")


class PanelB(bpy.types.Panel):
    bl_label = "Specials"
    bl_idname = "PT_PanelB"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My 1st Addon"
    bl_parent_id = "PT_TestPanel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.label(text="Select a Special Option", icon="RECORD_OFF")
        row = layout.row()
        row.operator("object.shade_smooth", icon="MOD_SMOOTH",
                     text="Set Smooth Shading")


def register():
    bpy.utils.register_class(TestPanel)
    bpy.utils.register_class(PanelA)
    bpy.utils.register_class(PanelB)


def unregister():
    bpy.utils.unregister_class(TestPanel)
    bpy.utils.unregister_class(PanelA)
    bpy.utils.unregister_class(PanelB)


if __name__ == "__main__":
    register()
