"""
Camera Tools

Some of the more basic stuff to create and work with cameras

"""
import pymel.core as pm


def create_render_cam(name="RENDER_CAM", exposure=True):
    """
    Creates a camera and renames it 
    
    str name: name of the camera
    bool exposure: connect a mia_exposure_photographic node to the camera     
    """
    if not pm.objExists(name):
        cam = pm.camera()[0]
        pm.rename(cam, name)
        [cam.renderable.set(cam.name().startswith(name)) for cam in pm.ls(cameras=True)]
    cam = pm.PyNode(name)
    
    if exposure:
        if not cam.miLensShader.isConnected():
            node = pm.createNode("mia_exposure_photographic")
            node.film_iso.set(800)
            node.f_number.set(1.2)
            node.gamma.set(1)
            pm.connectAttr(node.message, cam.miLensShader, force=True)
    
    cam.getShape().setDisplayResolution(True)
    pm.lookThru(name)
    
    pm.select(cam)


if __name__ == "__main__":
    create_render_cam()
