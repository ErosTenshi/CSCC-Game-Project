from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task

class Player(SphereCollideObject):
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Player, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1)
        self.taskMgr = taskMgr
        self.accept = accept
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
        self.SetKeyBindings()
    

    
    def SetKeyBindings(self):
        #All of our key bindings for our spaceship's movement.
        self.accept('w', self.Thrust, [1])
        self.accept('w-up', self.Thrust, [0])
        self.accept('q', self.LeftTurn, [1])
        self.accept('q-up', self.LeftTurn, [0])
        self.accept('e', self.RightTurn, [1])
        self.accept('e-up', self.RightTurn, [0])
        self.accept('space', self.ThrustUp, [1]) 
        self.accept('space-up', self.ThrustUp, [0])
        self.accept('s', self.ThrustBack, [1])
        self.accept('s-up', self.ThrustBack, [0])
        self.accept('d', self.ThrustRight, [1])
        self.accept('d-up', self.ThrustRight, [0])
        self.accept('a', self.ThrustLeft, [1])
        self.accept('a-up', self.ThrustLeft, [0]) 
        self.accept('shift', self.ThrustDown, [1])
        self.accept('shift-up', self.ThrustDown, [0])
    
    def ThrustBack(self, KeyDown):
        if KeyDown:
            self.taskMgr.add(self.ApplyThrustBack, 'backward-thrust')
        else:
            self.taskMgr.remove('backward-thrust')
    
    def ApplyThrustBack(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.back())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def Thrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskMgr.remove('forward-thrust')
    
    def ApplyThrust(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont 
    
    def ThrustUp(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrustUp, 'upward-thrust')
        else:
            self.taskMgr.remove('upward-thrust')
            
    def ApplyThrustUp(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.up())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def ThrustDown(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrustDown, 'downward-thrust')
        else:
            self.taskMgr.remove('downward-thrust')
    
    def ApplyThrustDown(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.down())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def ThrustRight(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrustRight, 'right-thrust')
        else:
            self.taskMgr.remove('right-thrust')
    
    def ApplyThrustRight(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.right())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def ThrustLeft(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrustLeft, 'left-thrust')
        else:
            self.taskMgr.remove('left-thrust')
    
    def ApplyThrustLeft(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.left())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def ApplyLeftTurn(self, task):
        #Half a degree every frame.
        rate = .5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
        
    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskMgr.remove('left-turn')
    
    
    def ApplyRightTurn(self, task):
        #Half a degree every frame.
        rate = -.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
        
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskMgr.remove('right-turn')