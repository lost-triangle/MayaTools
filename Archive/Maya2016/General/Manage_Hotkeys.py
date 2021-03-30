"""
Manage Hotkeys

Enables the ability to switch between different Keyboard shortcut layouts.

@author: Neal Buerger www.nealbuerger.com
"""

import pymel.core as pm


def reset_all_hotkeys():
    """
    Reset Hotkeys to Factory Settings
    """
    pm.hotkey(fs=True)


def set_hotkeys(lst):
    """
    Sets hotkeys based on list of key, command Tuples

    @param lst: List of (key, command) Tuples
    """
    for command in lst:
        key, name = command
        pm.hotkey(k=key, name=name)

def modelling_hotkeys(modelling_toolkit=True):
    """
    Bevel, Extrude and Split
    are mapped to b, n, m

    Maya 2014 is required to use the modelling Toolkit

    @param modelling_toolkit: hotkeys use modelling toolkit commands
    """
    if not pm.versions.current() >= pm.versions.v2014:
        raise ValueError

    if modelling_toolkit:
        pm.nameCommand('MT_Bevel', annotation='Modelling Toolkit Bevel', command='nexOpt -e manipType bevel;')
        pm.nameCommand('MT_Extrude', annotation ="Modelling Toolkit Extrude", command = 'nexOpt -e manipType extrude;')
        pm.nameCommand('MT_MultiCut', annotation ="Modelling Toolkit MultiCut", command = 'nexOpt -e manipType cut;')

        commands = [("b", "MT_Bevel"), ("n", "MT_Extrude"), ("m", "MT_MultiCut")]
    else:
        commands = [("b", "BevelPolygonNameCommand"), ("n", "PolyExtrude"), ("m", "SplitPolygonTool")]

    set_hotkeys(commands)


reset_all_hotkeys()


