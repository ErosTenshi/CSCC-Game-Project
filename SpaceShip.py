from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3, CollisionHandlerEvent, CollisionTraverser, CollisionNode
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
import re
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage, TransparencyAttrib
from direct.gui.DirectGui import DirectWaitBar
from direct.gui.OnscreenText import OnscreenText

class Player(SphereCollideObject):
    droneExplodeCount = 0
    def __init__(self, traverser, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, Render: NodePath):
        super(Player, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1)
        self.taskMgr = taskMgr
        self.accept = accept
        self.render = Render
        self.loader = loader
        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        self.reloadTime = .25
        self.missileDistance = 4000 # until the missile explodes
        self.missileBay = 1 # only one missile in the missile bay to be launched
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
        self.maxBoost = 5.0     
        self.boostLeft = self.maxBoost
        self.boosting = False
        self.boostCooldown = False
        self.boostSpeedMultiplier = 2.5  
        self.boostRate = 10             
        self.boostRechargeRate = 2      
        self.normalRate = 5             

        self.SetupBoostHUD()
        
        self.cntExplode = 0
        self.explodeIntervals = {}

        self.traverser = traverser
        
        self.handler = CollisionHandlerEvent()
        
        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)
        self.EnableHUD()
        self.SetKeyBindings()
        self.SetParticles()

    
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
        self.accept('f', self.Fire)
        self.accept('r', self.ActivateBoost)
    
    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        print("fromNode: " + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print("intoNode: " + intoNode)
        intoPosition = Vec3(entry.getSurfacePoint(self.render))
        
        tempVar = fromNode.split('_')
        print("tempVar: " + str(tempVar))
        shooter = tempVar[0]
        print("Shooter: " + str(shooter))
        tempVar = intoNode.split('-')
        print("TempVar1: " + str(tempVar))
        tempVar = intoNode.split('_')
        print("TempVar2 " + str(tempVar))
        victim = tempVar[0]
        print("Victim: " + str(victim))
        
        pattern = r'[0-9]'
        strippedString = re.sub(pattern, '', victim)        
        
        if (strippedString == "Drone" or strippedString == "Planet" or strippedString == "Space Station"):
            print(victim, ' hit at ', intoPosition)
            self.DestroyObject(victim, intoPosition)
            
                
            
        print(shooter + ' is DONE.')
        Missile.Intervals[shooter].finish()
        
    
    def DestroyObject(self, hitID, hitPosition):
        nodeID = self.render.find(hitID)
        nodeID.detachNode()
        
        #starts explosion
        self.explodeNode.setPos(hitPosition)
        self.Explode()
        ParticleEffect()
        
        if "Drone" in hitID:
            base.update_droneExplodeCount()
        
    def SetParticles(self):
        base.enableParticles()
        self.explodeEffect = ParticleEffect()
        self.explodeEffect.loadConfig('./Assets/ParticleEffects/Explosions/Basic_xpld_efx.ptf')
        self.explodeEffect.setScale(20)
        self.explodeNode = self.render.attachNewNode('ExplosionEffects')
    
    def Explode(self):
        self.cntExplode += 1
        tag = 'particles-' + str(self.cntExplode)
        
        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
        self.explodeIntervals[tag].start()
    
    def ExplodeLight(self, t):
        if t == 1.0 and self.explodeEffect:
            self.explodeEffect.disable()
        elif t == 0:
            self.explodeEffect.start(self.explodeNode)
        
    def Fire(self):
        if self.missileBay:
            self.Fire
        else:
            # if we are not reloading, we want to start reloading
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                # call the reload method on no delay.
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
        travRate = self.missileDistance
        aim = self.render.getRelativeVector(self.modelNode, Vec3.forward()) # the direction the spaceship is facing.
        aim.normalize() # normalizing the vector makes it consistent all the time.
        fireSolution = aim * travRate
        inFront = aim * 150
        travVec = fireSolution + self.modelNode.getPos()
        self.missileBay -= 1
        tag = 'Missile' + str(Missile.missileCount)
        posVec = self.modelNode.getPos() + inFront # spawn the missile in front of the nose of the ship.
        currentMissile = Missile(self.loader, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)
        # "fluid = 1" makes collision be checked between the last interval and this interval to make sure there's nothing in-between both checks that wasn't hit.
        Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
        Missile.Intervals[tag].start()
        
        self.traverser.addCollider(currentMissile.collisionNode, self.handler)
        
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            print('reload complete.')
            return Task.done
        elif task.time <= self.reloadTime:
            print('Reload Proceeding...')
            return Task.cont
        if self.missileBay > 1:
            self.missileBay = 1
    
    def CheckIntervals(self, task):
        for i in Missile.Intervals:
            # isPlaying returns true or false to see if the missile has gotten to the end of its path.
            if not Missile.Intervals[i].isPlaying():
                # if its path is done, we get rid of everything to do with that missile.
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print(i + 'has reached the end of its fire solution')
                # we break because when things are deleted from a dictionary, we have to refactor the dictionary so we can reuse it. This is because when we delete things, there is a gap at that point
                break
        return Task.cont
    
    
    
    def EnableHUD(self):
        
        self.Hud = OnscreenImage(image = "./Assets/Hud/Reticle3b.png", pos = Vec3(0, 0, 0), scale = 0.1)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)
        
        
    
    def ThrustBack(self, KeyDown):
        if KeyDown:
            self.taskMgr.add(self.ApplyThrustBack, 'backward-thrust')
        else:
            self.taskMgr.remove('backward-thrust')
    
    def ApplyThrustBack(self, task):
        rate = self.normalRate
        if self.boosting:
            rate *= self.boostSpeedMultiplier
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
        rate = self.normalRate
        if self.boosting:
            rate *= self.boostSpeedMultiplier
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
        rate = self.normalRate
        if self.boosting:
            rate *= self.boostSpeedMultiplier
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
        rate = self.normalRate
        if self.boosting:
            rate *= self.boostSpeedMultiplier
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
        rate = self.normalRate
        if self.boosting:
            rate *= self.boostSpeedMultiplier
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
        rate = self.normalRate
        if self.boosting:
            rate *= self.boostSpeedMultiplier
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

    def ActivateBoost(self):
        if not self.boostCooldown and self.boostLeft > 0:
            print("Boost activated!")
            self.boosting = True
            self.boostText.setText("BOOSTING!")
            self.taskMgr.add(self.ApplyBoost, 'boost-timer')

    def ApplyBoost(self, task):
        if self.boostLeft <= 0:
            print("Boost depleted.")
            self.boosting = False
            self.boostCooldown = True
            self.boostText.setText("RECHARGING...")
            self.taskMgr.doMethodLater(0.5, self.RechargeBoost, 'boost-recharge')
            return Task.done
        self.boostLeft -= globalClock.getDt() * self.boostRate
        self.UpdateBoostBar()
        return Task.cont

    def RechargeBoost(self, task):
        self.boostLeft += globalClock.getDt() * self.boostRechargeRate
        self.UpdateBoostBar()

        if self.boostLeft >= self.maxBoost:
            self.boostLeft = self.maxBoost
            self.boostCooldown = False
            self.boostText.setText("")
            return Task.done
        return Task.cont

    def UpdateBoostBar(self):
        percent = max(0, (self.boostLeft / self.maxBoost) * 100)
        self.boostBar['value'] = percent

    def SetupBoostHUD(self):
        self.boostBar = DirectWaitBar(text="", value=100, pos=(0, 0, -0.85), scale=0.3, barColor=(0.3, 0.7, 1.0, 1), frameColor=(0.2, 0.2, 0.2, 1))
        self.boostText = OnscreenText(text="", pos=(0, -0.95), fg=(1, 1, 0, 1), scale=0.07, mayChange=True)
