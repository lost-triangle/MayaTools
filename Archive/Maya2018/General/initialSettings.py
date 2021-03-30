import pymel.core as pm
import maya.cmds as cmds


def setInitialSettings():
    # Grid Settings
    pm.grid(size=50, displayPerspectiveLabels=True)
    pm.grid(default=True, size=50, displayPerspectiveLabels=True)

    # Enable Autosave
    pm.system.autoSave(enable=True, limitBackups=True, maxBackups=15)

    # Enable Infinite Undo
    pm.system.undoInfo(infinity=True)

    # Enable Poly Face Select with Center
    pm.modeling.polySelectConstraint(wholeSensitive=False)


if __name__ == "__main__":
    if pm.versions.current() >= 20180000:
        print "Hi"
        setInitialSettings()
