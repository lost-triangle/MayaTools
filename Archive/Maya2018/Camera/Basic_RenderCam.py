import pymel.core as pm
import maya.cmds as cmds

"""
Camera Tools

"""
class BasicCamera:
    """
    Basic repetitive Camera Tasks

    """
    @staticmethod
    def set_default_render_cam(name="RENDER_CAM"):
        """
        Sets the Global RenderCamera Attribute
        """
        for cam in pm.ls(cameras=True):
            cam.renderable.set(cam.name().startswith(name))
        

    @staticmethod
    def create_render_cam(name="RENDER_CAM"):
        """
        Creates a camera and renames it

        str name: name of the camera
        bool exposure: connect a mia_exposure_photographic node to the camera
        """
        if not pm.objExists(name):
            cam = pm.camera()[0]
            pm.rename(cam, name)
        BasicCamera.set_default_render_cam(name)
        cam = pm.PyNode(name)

        cam.getShape().setDisplayResolution(True)
        pm.lookThru(name)

        pm.select(cam)


if __name__ == "__main__":
    BasicCamera.create_render_cam()
