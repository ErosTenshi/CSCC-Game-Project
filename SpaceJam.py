from direct.showbase.ShowBase import ShowBase
import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import SpaceShip 
from typing import Callable
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionNode, Vec3
import math, random, sys
from direct.task import Task


class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Sets up Universe model and texture
        self.Universe = spaceJamClasses.Universe(self.loader, "Assets/Universe/Universe.x", self.render, 'Universe', "Assets/Universe/Universe.jpg", (0, 0, 0), 15000)
        
        # Sets up Planet 1 model, texture, and location/position
        self.Planet1 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet1', "Assets/Planets/PlanetPsy.png", (150, 5000, 67), 350)
        
        self.Planet2 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet2', "Assets/Planets/PlanetYinYang.png", (1150, 5000, 1067), 350)
        
        self.Planet3 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet3', "Assets/Planets/PlanetCleo.png", (2150, 5000, 2067), 350)
        
        self.Planet4 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet4', "Assets/Planets/PlanetGamma.png", (3150, 5000, 3067), 350)
        
        self.Planet5 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet5', "Assets/Planets/PlanetRadia.png", (4150, 5000, 4067), 350)
        
        self.Planet6 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet6', "Assets/Planets/PlanetSangre.png", (5150, 5000, 5067), 350)
        
        # Sets up Space Station model, texture, and location/position
        self.SpaceStation = spaceJamClasses.SpaceStation(self.loader, "Assets/SpaceStation/spaceStation.x", self.render, 'Space Station', "Assets/SpaceStation/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)

        # Sets up Spaceship model, texture, and location/position.
        self.SpaceShip = SpaceShip.Player(self.loader, self.taskMgr, self.accept, "Assets/Spaceships/spacejet.3ds", self.render, 'Space Ship', "Assets/Spaceships/spacejet_C.png", Vec3(1000, 1200, -550), 50, self.render)
        self.SpaceShip.SetKeyBindings()
        
        self.Drone = spaceJamClasses.Drone(self.loader, "Assets/DroneDefender/DroneDefender.x", self.render, 'Drones', "Assets/DroneDefender/Drones.jpg", (1000, 1200, 0), 50)
        
        self.CircleDrone = self.loader.loadModel("Assets/DroneDefender/DroneDefender.x")
        
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.SpaceShip.collisionNode, self.SpaceShip.modelNode)
        self.cTrav.addCollider(self.SpaceShip.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)
        
        
        
        
        x = 0
        for i in range(105):
            theta = x
            self.CircleX = self.render.attachNewNode('CircleX')
            self.CircleX.setPos(50.0 * math.cos(theta), 50.0 * math.sin(theta), 0.0 * math.tan(theta))
            self.CircleX.setColorScale(1.0, 0.0, 0.0, 1.0)
            self.CircleDrone.instanceTo(self.CircleX)
            
            x = x + 1
            
        y = 0
        for i in range(105):
            theta = y
            self.CircleY = self.render.attachNewNode('CircleY')
            self.CircleY.setPos(50.0 * math.sin(theta), 0.0 * math.tan(theta), 50.0 * math.cos(theta))
            self.CircleY.setColorScale(0.0, 1.0, 0.0, 1.0)
            
            self.CircleDrone.instanceTo(self.CircleY)
            y = y + 1
        
        z = 0
        for i in range(105):
            theta = z
            self.CircleZ = self.render.attachNewNode('CircleZ')
            self.CircleZ.setPos(0.0 * math.tan(theta), 50.0 * math.cos(theta), 50.0 * math.sin(theta))
            self.CircleZ.setColorScale(0.0, 0.0, 1.0, 1.0)
            
            self.CircleDrone.instanceTo(self.CircleZ)
            z = z + 1
        
        
        fullCycle = 60
        
        for j in range(fullCycle): 
            spaceJamClasses.Drone.droneCount += 0
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.SpaceStation, nickName, j, fullCycle, 2)
     
        
    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "Assets/DroneDefender/octotoad1_auv.png", position, 5)
        
    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "Assets/DroneDefender/octotoad1_auv.png", position, 10)
    
    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.SpaceShip.modelNode)
        self.camera.setFluidPos(0, 1, 0)
    
        
        
        
    def quit(self):
        sys.exit()  
         
app = MyGame()
app.SetCamera()
app.run()
