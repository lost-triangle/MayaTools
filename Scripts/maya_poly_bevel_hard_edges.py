import pymel.core as pm

def obj_is_poly(obj):
    #Evaluates if Object is Polygon
    return pm.nodeType(obj) == "mesh"

def bevelHardEdges(obj, offset = 0.5, segments = 1):
    if obj_is_poly(obj):
        pm.select(obj)
        pm.polySelectConstraint( m=3, t=0x8000, sm=1 ) # to get hard edges
        pm.polyBevel(offset = offset, segments = segments,autoFit = True, offsetAsFraction = True, fillNgons = True)

def bevelHardEdgesOnSelected():
    for item in pm.selected():
        bevelHardEdges(item.getShape())

bevelHardEdgesOnSelected()