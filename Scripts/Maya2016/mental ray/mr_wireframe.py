"""
Renders a wireframe image using mental ray

Created on Jul 6, 2013

@author: Neal Buerger
"""
import pymel.core as pm
import subprocess
import os


def find_render_cam():
    """
    Finds current rendercam or returns "persp"

    @rtype : Camera
    """
    for cam in pm.ls(cameras=True):
        if cam.renderable.get():
            return cam
    pm.PyNode("persp").renderable.set(True)
    return pm.PyNode("persp")


def create_wireframe_rl(name="wireframe"):
    """
    Creates wireframe material
    Creates wireframe layer
    Adds all geometry and rendercam to the renderlayer
    
    @param name: str layername
    """
    mat_name = "%s_mat" % name

    if not pm.objExists(mat_name):        
        material_node = pm.shadingNode("lambert", n=mat_name, asShader=True)
        material_node.setColor([1, 1, 1])
        
        material_sg_node = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name="%sSG" % mat_name)
        material_sg_node.miContourEnable.set(1)
        material_sg_node.miContourColor.set([0,0,0])
        material_sg_node.miContourWidth.set(1.5)
        material_node.outColor >> material_sg_node.surfaceShader
        
        if not pm.objExists(name):
            render_layer = pm.createRenderLayer(n=name)
            render_layer.setCurrent()
            render_layer.addMembers(pm.ls(geometry=True, cameras=True))
            material_sg_node.message >> render_layer.shadingGroupOverride


def render_wireframe():
    """
    Renders Renderlayer using Mental Ray Legacy options

    """
    pm.mel.miCreateDefaultNodes()

    render_globals = pm.PyNode("defaultRenderGlobals")
    render_globals.currentRenderer.set("mentalRay")
    render_globals.imageFormat.set(3)
    
    #Legacy Options
    mentalray_options = pm.PyNode("miDefaultOptions")
    mentalray_options.miRenderUsing.set(2)
    pm.mel.miSetRenderUsingValue()
    mentalray_options.maxSamples.set(2)

    pm.PyNode("miDefaultFramebuffer").contourEnable.set(1)
    mentalray_options.contourPriData.set(1)
    
    #Set Camera options
    render_cam = "RENDER_CAM"
    if not pm.objExists(render_cam):
        render_cam = find_render_cam()
    [cam.renderable.set(render_cam == cam.name()) for cam in pm.ls(cameras=True)]
    
    pm.editRenderLayerAdjustment(pm.PyNode(render_cam).backgroundColor)
    pm.PyNode(render_cam).backgroundColor.set([1, 1, 1])
    pm.runtime.RenderViewWindow()
    
    #Render Image
    f = pm.Mayatomr(pv=True, layer="wireframe")
    f = os.path.normcase(f)
    os.system("open %s" % f)
    subprocess.Popen(r'explorer /select,"%s"' %f)
    
    #Reset to Unified Sampling
    mentalray_options.miRenderUsing.set(0)
    pm.PyNode("miDefaultFramebuffer").contourEnable.set(0)   

if __name__ == "__main__":
    create_wireframe_rl()
    render_wireframe()
