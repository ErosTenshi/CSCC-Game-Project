from direct.showbase.ShowBase import ShowBase

class SetupScene(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.Universe = self.loader.loadModel("Assets/Universe/Universe.x")
        self.Universe.reparentTo(self.render)
        self.Universe.setScale(15000)
        tex = self.loader.loadTexture("Assets/Universe/Universe.jpg")
        self.Universe.setTexture(tex, 1)
        
        self.Planet1 = self.loader.loadModel("Assets/Planets/protoPlanet.x")
        self.Planet1.reparentTo(self.render)
        self.Planet1.setPos(150, 5000, 67)
        self.Planet1.setScale(350)
        
        self.Planet2 = self.loader.loadModel("Assets/Planets/protoPlanet.x")
        self.Planet2.reparentTo(self.render)
        self.Planet2.setPos(1150, 5000, 67)
        self.Planet2.setScale(350)
        
        self.Planet3 = self.loader.loadModel("Assets/Planets/protoPlanet.x")
        self.Planet3.reparentTo(self.render)
        self.Planet3.setPos(2150, 5000, 67)
        self.Planet3.setScale(350)
        
        self.Planet4 = self.loader.loadModel("Assets/Planets/protoPlanet.x")
        self.Planet4.reparentTo(self.render)
        self.Planet4.setPos(3150, 5000, 67)
        self.Planet4.setScale(350)
        
        self.Planet5 = self.loader.loadModel("Assets/Planets/protoPlanet.x")
        self.Planet5.reparentTo(self.render)
        self.Planet5.setPos(4150, 5000, 67)
        self.Planet5.setScale(350)
        
        self.Planet6 = self.loader.loadModel("Assets/Planets/protoPlanet.x")
        self.Planet6.reparentTo(self.render)
        self.Planet6.setPos(5150, 5000, 67)
        self.Planet6.setScale(350)

app = SetupScene()
app.run()