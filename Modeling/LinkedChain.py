'''
Linked Chain

Creates a Torus like object, links them together as linked Chain and positions the chain along a curve

Example:
1. Select a curve in Maya
2. Execute command:
Poly_Linked_Chain(radius = 1, sectionradius =0.1, extrude = 1, variation = 20, name="chain").createChainForSelectedCurve()
or:
Poly_Linked_Chain().createChainForSelectedCurve()

Created on May 7, 2013

@author: Neal Buerger www.nealbuerger.com
'''
import pymel.core as pm
import random

class Poly_Linked_Chain:
    
    def __init__(self, **kwargs):
        """
        Accepts following Keywords:
        radius: of the Torus created (Default 1)
        sectionradius: of the Torus (Default 0.1)
        extrude: length of the torus extrusion (Default 0)
        variation: along the rotation of the linked elements (Default 0)
        name: name of the chain (Default chain)
        """
        
        self.radius = kwargs.get("radius" ,1)
        self.sectionradius = kwargs.get("sectionradius" ,0.1)
        self.extrude = kwargs.get("extrude" ,0)
        self.variation = kwargs.get("variation" ,0)
        if self.variation < 0:
            self.variation = abs(self.variation)
        if  self.variation > 45:
            self.variation = 45
        
        self.name = kwargs.get("name" , "chain")
    
    def createLink(self):
        """
        creates a Torus and extrudes half of it
        To be used as alternative to a provided geometry
        
        """
        basechain = pm.polyTorus(radius = self.radius, sr = self.sectionradius, tw= 0, sx = 20, sy = 20, ax = (0,1,0), ch = 1)[0]    
        if self.extrude is not 0:
            faces = []
            for j in basechain.vtx:
                if j.getPosition()[0] > 0:
                    faces.append(j.connectedFaces())
            pm.polyExtrudeFacet(faces, translateX=self.extrude)
        return basechain
        
    
    def makeChain(self, obj, linklenght, chainlenght, preserveObj = False):
        """
        Uses provided geometry to create a straight chain
        
        obj: object to be used for the chain
        linklenght: lenght of the obj
        chainlenght: number of links that are created
        """
        if preserveObj:
            obj = pm.duplicate(obj, un=True)[0]
        pm.move(obj, 0,0,0)
        chain = [obj]
            
        rotValue = 0
        for i in range(1, chainlenght):
            obj = pm.duplicate(chain[0])[0]
            rotValue += 90 + random.randint(-self.variation, self.variation)
            if rotValue >= 360:
                rotValue -= 360
            pm.rotate(obj, [rotValue, 0, 0])        
            distance = linklenght * i
            pm.move(obj, distance,0,0)
            chain.append(obj)
        return chain
    
    def rigChain(self, chain):
        """
        takes chain and adds joints and a smooth bind to rig it
        
        chain: list of objects 
        """
        pm.select(deselect = True)
        jnts = []
        for obj in chain:
            pos = obj.translateX.get(), obj.translateY.get(), obj.translateZ.get() 
            jnts.append(pm.joint(p = pos))
            pm.rename(jnts[-1], self.name + "_joint%d" %  len(jnts))
        linked = pm.polyUnite(chain, n = self.name, ch = 0)[0]
        pm.skinCluster(linked, jnts[0])
        return jnts
    
    def createChainForCurve(self, crv, obj = None, linklenght = 1):
        """
        Uses the Curve and creates a chain based on the object that is passed into the function
        
        crv = curve to be used
        obj = object to be used
        linklength = lenght of the obj
        """
                
        if obj is None:
            obj = self.createLink()
            linklenght = (2*(self.radius - self.sectionradius*2)+self.extrude)
        chainlenght = int(pm.PyNode(crv).length()/linklenght)
        chain = self.makeChain(obj = obj, linklenght = linklenght, chainlenght = chainlenght)
        jnts = self.rigChain(chain)
        
        ik = pm.ikHandle( startJoint=jnts[0], endEffector=jnts[-1], solver='ikSplineSolver', createCurve=False, curve=crv, n = "%s_ikHandle%d" % (self.name, (len(pm.ls(regex= "%s_ikHandle.*" % self.name))+1)))    
        ctrlgrp = pm.group(jnts[0], ik[0], n = "%sctrl_grp" % self.name)
        print pm.listAttr(ctrlgrp)
        ctrlgrp.v.set(False)
        grpname = pm.group(crv, self.name, ctrlgrp, n = "%s_grp" % self.name)
        pm.select(crv)
        return grpname
    
    
    def createChainForSelectedCurve(self):
        for i in pm.ls(sl =True, tr=True):
            if pm.nodeType(i.getShape()) == "nurbsCurve":
                self.createChainForCurve(i)
          
