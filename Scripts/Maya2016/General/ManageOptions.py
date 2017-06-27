import pymel.core as pm


def manage_default_options(**kwargs):
    """
    Sets Various Default options for Maya

    viewmManip : Default Hide the manipulator Cube
    gradient: Default Hide the Background gradient
    autosave: Default Enable Autosave
    mentalray: Default Enable mr as Default Render Engine
    interactiveCreation: Enables Disables Interactive Creation Mode for Primitive Objects

    hardware2: Optional Enable Hardware Renderer 2.0 as Default Render Engine

    """

    # Disable View Cube
    pm.viewManip(visible=kwargs.get("viewManip", False))

    # Disable Background Gradient
    pm.displayPref(displayGradient=kwargs.get("gradient", False))

    # Infinite Undo
    pm.undoInfo(state=True, infinity=kwargs.get("infiniteUndo", True))

    # Enable Autosave, max Versions 10, interval 15min
    pm.autoSave(enable=kwargs.get("autosave", True), maxBackups=kwargs.get(
        "maxBackups", 10), interval=kwargs.get("interval", 900))

    # Activate Mental Ray
    if kwargs.get("mentalray", True):
        enable_mr_plugin()

    # Sets Hardwarerenderer 2.0 as Default
    if kwargs.get("hardware2", False):
        pm.PyNode("defaultRenderGlobals").currentRenderer.set("mayaHardware2")

    # Expose Mental Ray Production Nodes
    pm.optionVar["MIP_SHD_EXPOSE"] = 1

    # Disable Interactive Creation
    set_interactive_creation(kwargs.get("interactiveCreation", False))


def set_interactive_creation(enabled=False):
    """
    Enables or Disables Interactive Creation
    """
    pm.optionVar['createNurbsPrimitiveAsTool'] = enabled
    pm.ui.CommandMenuItem(
        "MayaWindow|mainCreateMenu|menuItem285|toggleCreateNurbsPrimitivesAsToolItem").setCheckBox(enabled)

    pm.optionVar['createPolyPrimitiveAsTool'] = enabled
    pm.ui.CommandMenuItem(
        "MayaWindow|mainCreateMenu|polyPrimitivesItem|toggleCreatePolyPrimitivesAsToolItem").setCheckBox(enabled)


def enable_mr_plugin():
    """
    loads and sets the mental Ray Plugin as default
    """
    load_plugin('Mayatomr')
    pm.PyNode("defaultRenderGlobals").currentRenderer.set("mentalRay")
    print('# Result: mental ray Plugin loaded #')


def load_plugin(plugin_name):
    """
    if the plugin is not loaded, it is loaded and set to autoload

    pluginName: name of the plugin to be loaded
    """
    if not pm.pluginInfo(plugin_name, q=True, loaded=True):
        pm.loadPlugin(plugin_name)
        pm.pluginInfo(plugin_name, edit=True, autoload=True)

if __name__ == "__main__":
    manage_default_options()
