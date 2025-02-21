from direct.showbase.BufferViewer import taskMgr
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, Vec3
from direct.task import Task


class Planet(ShowBase):
    def __init__(self, loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Universe(ShowBase):
    def __init__(self, loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
    
class SpaceShip(ShowBase):
    def __init__(self, loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.taskManager = Task.TaskManager()
    
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
        self.accept('s', self.ThrustDown, [1])
        self.accept('s-up', self.ThrustDown, [0])
        self.accept('d', self.ThrustRight, [1])
        self.accept('d-up', self.ThrustRight, [0])
        self.accept('a', self.ThrustLeft, [1])
        self.accept('a-up', self.ThrustLeft, [0]) 
    
    def Thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskManager.remove('forward-thrust')
    
    def ApplyThrust(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont 
    
    def ThrustUp(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrustUp, 'upward-thrust')
        else:
            self.taskManager.remove('upward-thrust')
            
    def ApplyThrustUp(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.up())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def ThrustDown(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrustDown, 'downward-thrust')
        else:
            self.taskManager.remove('downward-thrust')
    
    def ApplyThrustDown(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.down())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def ThrustRight(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrustRight, 'right-thrust')
        else:
            self.taskManager.remove('right-thrust')
    
    def ApplyThrustRight(self, task):
        rate = 5
        trajectory = self.modelNode.getRelativeVector(self.modelNode, Vec3.right())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def ThrustLeft(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrustLeft, 'left-thrust')
        else:
            self.taskManager.remove('left-thrust')
    
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
            self.taskManager.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskManager.remove('left-turn')
    
    
    def ApplyRightTurn(self, task):
        #Half a degree every frame.
        rate = -.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
        
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskManager.remove('right-turn')  
      
    
        
    
class SpaceStation(ShowBase):
    def __init__(self, loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)   
      
class Drone(ShowBase):
    # How many drones have spawned
    droneCount = 0
    def __init__(self, loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
    