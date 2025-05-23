from direct.showbase.ShowBase import ShowBase
import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import SpaceShip 
from typing import Callable
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionNode, Vec3, TextNode
import math, random, sys
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectFrame, DirectButton


class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.main_menu = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-1, 1, -1, 1))
        self.start_button = DirectButton(text="Start Game", scale=0.1, pos=(0, 0, 0.2), command=self.start_game, parent=self.main_menu)
        self.quit_button = DirectButton(text="Quit Game", scale=0.1, pos=(0, 0, -0.2), command=sys.exit, parent=self.main_menu)
        
    def start_game(self):
        self.main_menu.hide()
        self.Universe = spaceJamClasses.Universe(self.loader, "Assets/Universe/Universe.x", self.render, 'Universe', "Assets/Universe/Universe.jpg", (0, 0, 0), 15000)
        
        self.Planet1 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet1', "Assets/Planets/PlanetPsy.jpg", (150, 5000, 67), 350)
        
        self.Planet2 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet2', "Assets/Planets/PlanetYinYang.jpg", (1150, 5000, 1067), 350)
        
        self.Planet3 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet3', "Assets/Planets/PlanetCleo.jpg", (2150, 5000, 2067), 350)
        
        self.Planet4 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet4', "Assets/Planets/PlanetGamma.jpg", (3150, 5000, 3067), 350)
        
        self.Planet5 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet5', "Assets/Planets/PlanetRadia.jpg", (4150, 5000, 4067), 350)
        
        self.Planet6 = spaceJamClasses.Planet(self.loader, "Assets/Planets/protoPlanet.x", self.render, 'Planet6', "Assets/Planets/PlanetSangre.jpg", (5150, 5000, 5067), 350)
        
        
        self.SpaceStation = spaceJamClasses.SpaceStation(self.loader, "Assets/SpaceStation/spaceStation.x", self.render, 'Space Station', "Assets/SpaceStation/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)

    
        
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        
        self.SpaceShip = SpaceShip.Player(self.cTrav, self.loader, self.taskMgr, self.accept, "Assets/Spaceships/spacejet.3ds", self.render, 'Space Ship', "Assets/Spaceships/spacejet_C.png", Vec3(1000, 1200, -550), 50, self.render)
        self.SpaceShip.SetKeyBindings()
        
        self.is_first_person = True
        self.accept('p', self.ThirdPerson) #Keybinds for First and Third Person Perspectives
        self.accept('o', self.FirstPerson)
        self.setup_game_elements()
        self.FirstPerson()
        
        self.Sentinal1 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, "Assets/DroneDefender/octotoad1_auv.png", self.Planet5, 900, "MLB", self.SpaceShip)
        self.Sentinal2 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, "Assets/DroneDefender/octotoad1_auv.png", self.Planet2, 500, "Cloud", self.SpaceShip)
        self.Sentinal3 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, "Assets/DroneDefender/octotoad1_auv.png", self.Planet3, 900, "MLB", self.SpaceShip)
        self.Sentinal4 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, "Assets/DroneDefender/octotoad1_auv.png", self.Planet4, 500, "Cloud", self.SpaceShip)
        
        self.Wanderer1 = spaceJamClasses.Wanderer(self.loader, "Assets/DroneDefender/DroneDefender.x", self.render, "Drone", 6.0, "Assets/DroneDefender/octotoad1_auv.png", self.SpaceShip)
        self.Wanderer2 = spaceJamClasses.Wanderer2(self.loader, "Assets/DroneDefender/DroneDefender.x", self.render, "Drone", 6.0, "Assets/DroneDefender/octotoad1_auv.png", self.SpaceShip)
        
    def setup_game_elements(self):
        self.Drone = spaceJamClasses.Drone(self.loader, "Assets/DroneDefender/DroneDefender.x", self.render, 'Drone', "Assets/DroneDefender/Drones.jpg", (1000, 1200, 0), 50)
        
        self.CircleDrone = self.loader.loadModel("Assets/DroneDefender/DroneDefender.x", 1)
        
        
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.SpaceShip.collisionNode, self.SpaceShip.modelNode)
        self.cTrav.addCollider(self.SpaceShip.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)
        
        self.elapsed_time = 0
        self.timer_text = OnscreenText(text="Time: 0s", pos=(-1.2, 0.9), scale=0.07, fg=(1, 1, 1, 1), align=TextNode.A_left)
        self.droneExplodeCount_text = OnscreenText(text="Destroyed Drones: " + str(SpaceShip.Player.droneExplodeCount), pos=(-1.2, 0.8), scale=0.07, fg=(1, 1, 1, 1), align=TextNode.A_left)
        self.taskMgr.add(self.update_timer, "updateTimerTask")
        
        self.exit_menu = DirectFrame(frameColor=(0, 0, 0, 0.7), frameSize=(-0.5, 0.5, -0.3, 0.3), pos=(0, 0, 0))
        self.exit_button = DirectButton(text="Exit Game", scale=0.07, pos=(0, 0, 0.1), command=self.quit_game, parent=self.exit_menu)
        self.cancel_button = DirectButton(text="Cancel", scale=0.07, pos=(0, 0, -0.1), command=self.hide_exit_menu, parent=self.exit_menu)
        self.exit_menu.hide()
        self.accept("escape", self.show_exit_menu)
        
          
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
            spaceJamClasses.Drone.droneCount += 2
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount + 1)
            self.DrawBaseballSeams(self.SpaceStation, nickName, j, fullCycle, 2)    
        
    def show_exit_menu(self):
        self.exit_menu.show()
    
    def hide_exit_menu(self):
        self.exit_menu.hide() 
    
    def quit_game(self):
        sys.exit()
    
    def update_timer(self, task):
        self.elapsed_time = int(task.time)
        self.timer_text.setText(f"Time: {self.elapsed_time}s")
        return task.cont
        
    def update_droneExplodeCount(self):
        SpaceShip.Player.droneExplodeCount += 1
        self.droneExplodeCount_text.setText(f"Drones Destroyed: {SpaceShip.Player.droneExplodeCount}")    
        
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
    
    def FirstPerson(self):
        self.disableMouse()
        self.is_first_person
            # First-person mod
        self.camera.reparentTo(self.SpaceShip.modelNode)
        self.camera.setFluidPos(0, 1, 0)  # Adjust to a first-person view
        
    def ThirdPerson(self):
        self.camera.reparentTo(self.SpaceShip.modelNode)
        self.camera.setPos(self.SpaceShip.modelNode.getPos() + Vec3(-10, -10, 0))  # Set camera position behind the ship
        self.camera.setFluidPos(0, -50, 5)

    
        
    def quit(self):
        sys.exit()  
         
app = MyGame()
app.run()