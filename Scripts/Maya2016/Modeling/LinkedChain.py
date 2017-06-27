"""
Linked Chain

Creates a Torus like object, links them together as linked Chain and positions the chain along a curve

Example:
1. Select a curve in Maya
2. Execute command:

Poly_Linked_Chain(radius = 1, sectionradius =0.1, extrude = 1, variation = 20, name="chain").createChainForSelectedCurve()

Created on May 7, 2013

@author: Neal Buerger www.nealbuerger.com
"""
import pymel.core as pm
import random


class PolyLinkedChain:
    
    def __init__(self, **kwargs):
        """
        Accepts following Keywords:
        radius: of the Torus created (Default 1)
        section_radius: of the Torus (Default 0.1)
        extrude: length of the torus extrusion (Default 0)
        variation: along the rotation of the linked elements (Default 0)
        name: name of the chain (Default chain)
        """
        
        self.radius = kwargs.get("radius", 1)
        self.section_radius = kwargs.get("section_radius", 0.1)
        self.extrude = kwargs.get("extrude", 0)
        self.variation = kwargs.get("variation", 0)
        if self.variation < 0:
            self.variation = abs(self.variation)
        if self.variation > 45:
            self.variation = 45
        
        self.name = kwargs.get("name" , "chain")
        self.name += str(len(pm.ls(regex="%s\d*" % self.name)) + 1)

    def create_link(self):
        """
        creates a Torus and extrudes half of it
        To be used as alternative to a provided geometry
        
        """
        base_chain = pm.polyTorus(radius=self.radius, sr=self.section_radius, tw=0, sx=20, sy=20, ax=(0, 1, 0), ch = 1)[0]
        if self.extrude is not 0:
            faces = []
            for j in base_chain.vtx:
                if j.getPosition()[0] > 0:
                    faces.append(j.connectedFaces())
            pm.polyExtrudeFacet(faces, translateX=self.extrude)
        return base_chain
        
    def make_chain(self, obj, link_length, chain_length, preserve_object=False):
        """
        Uses provided geometry to create a straight chain
        
        obj: object to be used for the chain
        linklenght: lenght of the obj
        chainlenght: number of links that are created
        """
        if preserve_object:
            obj = pm.duplicate(obj, un=True)[0]
        pm.move(obj, 0, 0, 0)
        chain = [obj]
            
        rotation_value = 0
        for i in range(1, chain_length):
            obj = pm.duplicate(chain[0])[0]
            rotation_value += 90 + random.randint(-self.variation, self.variation)
            if rotation_value >= 360:
                rotation_value -= 360
            pm.rotate(obj, [rotation_value, 0, 0])
            distance = link_length * i
            pm.move(obj, distance, 0, 0)
            chain.append(obj)
        return chain
    
    def rig_chain(self, chain):
        """
        takes chain and adds joints and a smooth bind to rig it
        
        chain: list of objects 
        """
        pm.select(deselect=True)
        joints = []
        for obj in chain:
            pos = obj.translateX.get(), obj.translateY.get(), obj.translateZ.get()
            jnt = pm.joint(p=pos)
            joints.append(jnt)
            pm.rename(jnt, self.name + "_joint%d" % len(joints))
        linked = pm.polyUnite(chain, ch=0)[0]
        self.name = pm.rename(linked, self.name)
        pm.skinCluster(linked, joints[0])
        return joints
    
    @staticmethod
    def add_cluster_handles(crv):
        """
        Adds Cluster Handles to Curve for every cv
        """
        for i in crv.cv:
            pm.parent(pm.cluster(i), crv)
    
    def create_chain_for_curve(self, crv, obj=None, link_length=1):
        """
        Uses the Curve and creates a chain based on the object that is passed into the function
        
        crv = curve to be used
        obj = object to be used
        linklength = lenght of the obj
        """
                
        if obj is None:
            obj = self.create_link()
            link_length = (2*(self.radius - self.section_radius*2)+self.extrude)
        chain_length = int(pm.PyNode(crv).length()/link_length)
        chain = self.make_chain(obj=obj, link_length=link_length, chain_length=chain_length)
        joints = self.rig_chain(chain)
        
        ik = pm.ikHandle(startJoint=joints[0], endEffector=joints[-1], solver='ikSplineSolver', createCurve=False, curve=crv)[0]
        pm.rename(ik, self.name + "_ikHandle")
            
        control_group = pm.group(joints[0], ik, n="%sctrl_grp" % self.name)
        control_group.v.set(False)
        pm.group(crv, self.name, control_group, n="%s_grp" % self.name)
        
        self.add_cluster_handles(crv)
        pm.select(deselect=True)
        
        return self.name

    def create_chain_for_selected_curve(self):
        """
        Creates Chains for selected curves
        """
        return [self.create_chain_for_curve(i) for i in pm.ls(sl =True, tr=True) if pm.nodeType(i.getShape()) == "nurbsCurve"]

    @staticmethod
    def delete_rig(name):
        """
        Removes Rig from geometry
        
        name: name of geometry
        """
        parent = pm.PyNode(name).getParent()
        pm.delete(name, ch=True)
        pm.parent(name, w=True)
        pm.delete(parent)