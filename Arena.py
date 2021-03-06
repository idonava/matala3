import random
import Robot
import copy
import Tkinter as tk
import simulator
import tkMessageBox
import GlobalParameters as GP


class Arena:

    def __init__(self):     #Constractur
        self.numOfRobots=0
        self.id = id
        self.X = GP.arenaX
        self.Y = GP.arenaY
        self.matrix=[[GP.white for x in range(self.X)]for y in range(self.Y)]
        self.movingRob = []
        self.staticRob = []
        self.numOfStatics = GP.numOfStatic
        self.numOfMoving = GP.numOMoving
        self.robs=[]
        self.recRob = []
        self.isMoving = False
        self.root = tk.Tk()
        self.configCanvas()
        self.root.state('zoomed')

    def configCanvas(self):     #Initial the canvas.
        self.canvas = tk.Canvas(self.root, width=1000, height=1000, scrollregion=(0, 0, 1050, 1050))
        self.addMenus()
        self.addScroll()
        self.canvas.pack(side='left', expand='True', fill='both')

    def addScroll(self):
        self.vbar = tk.Scrollbar(self.canvas, orient='vertical')
        self.vbar.pack(side='right', fill='y')
        self.vbar.config(command=self.canvas.yview)

    def addMenus(self):         #Add menu to the program.
        for i in range(11):
            x = (i * 100)
            self.canvas.create_line(x, 10, x, 0, width=2)
            self.canvas.create_text(x, 20, text='%d' % (100 * i), anchor="n")
        for i in range(10):
            y = 1000 - (i * 100)
            self.canvas.create_line(0, y, 10, y, width=2)
            self.canvas.create_text(40, y, text='%5.1f' % (1000 - (100 * i)), anchor="e")
        self.MenuBar = tk.Menu(self.root)
        self.men = tk.Menu(self.MenuBar, tearoff=0)
        self.men.add_command(label="Start", command=self.startMoving)
        self.men.add_command(label="Pause", command=self.pauseMoving)
        self.MenuBar.add_cascade(label="Test", menu=self.men)
        self.root.config(menu=self.MenuBar)


    def onObjectClick(self,event):      #Add information when clicked on robot.
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = int(self.canvas.gettags(item)[0])
        print("ID: ", tags)
        for rob in self.staticRob:
            if rob[0].id==tags:
                robot=rob
                break
        for rob in self.movingRob:
            if rob[0].id == tags:
                robot = rob
                break
        if robot[0].isStatic:
            string = "Actual Position: " + str(robot[1]) + " " + str(robot[2])
            tkMessageBox.showinfo("Static Robot ID: "+ str(tags), string)
        else:
            string="Actual Position: "+str(robot[1])+" "+str(robot[2])+"\n\nGuess position: "+str(robot[0].X)+" "+str(
                robot[0].Y) +"\n\nBatery: "+str(robot[0].Battery.bat)+ "%\n close robot: " + str(robot[0].closeRobot)
            tkMessageBox.showinfo("Moving Robot ID: "+str(tags),string )

        print(event.widget.find_closest(event.x, event.y))



    def startMoving(self):      #Start the moving in the GUI.
        self.isMoving = True
        simulator.moveRobot(self)

    def pauseMoving(self):   # Stop the moving in the GUI.
        self.isMoving = False

    def create_arena_from_file(self,fileName):  #Read the incoming file and create the robots arena
        i=0
        with open (fileName,'r') as f:
            lines=f.readlines()
        self.X=int(lines[i].split('=',1)[1])
        i=i+1
        self.Y = int(lines[i].split('=', 1)[1])
        i=i+1
        self.create_boundaries()
        numOfBlack = int(lines[i].split(':', 1)[1])
        i=i+1
        rectangleList=[]
        for x in range(numOfBlack):
            list1=lines[i].split('->')
            i=i+1
            for num in list1:
                list2=num.split(',')
                rectangleList.append(int(list2[0]))
                rectangleList.append(int(list2[1]))
            rect=self.canvas.create_rectangle(rectangleList[0],rectangleList[1],rectangleList[2],rectangleList[3], fill='black',tags='black')
            self.canvas.tag_bind(rect, '<ButtonPress-1>', self.onObjectClick)
            for x in range(rectangleList[0],rectangleList[2]+1):
                for y in range(rectangleList[1],rectangleList[3]+1):
                    self.matrix[x][y] = 2
            rectangleList = []
        numOfGray = int(lines[i].split(':', 1)[1])
        i = i + 1
        rectangleList = []
        for x in range(numOfGray):
            list1 = lines[i].split('->')
            i = i + 1
            for num in list1:
                list2 = num.split(',')
                rectangleList.append(int(list2[0]))
                rectangleList.append(int(list2[1]))
            self.canvas.create_rectangle(rectangleList[0], rectangleList[1], rectangleList[2], rectangleList[3], fill='gray')
            for x in range(rectangleList[0], rectangleList[2]+1):
                for y in range(rectangleList[1], rectangleList[3]+1):
                    self.matrix[x][y] = 1
            rectangleList = []
        self.numOfStatics = int(lines[i].split('=',1)[1])
        i=i+1
        self.numOfMoving = int(lines[i].split('=',1)[1])
        self.matrixWithoutRobots=copy.deepcopy(self.matrix)

    def create_boundaries(self):            #Create the boundaries from the incoming file.
        self.matrix = [[GP.white for x in range(self.X)] for y in range(self.Y)]
        for x in range(self.X):
            self.matrix[x][self.Y - 1] = GP.black
            self.matrix[x][0] = GP.black
        for y in range(self.Y):
            self.matrix[self.X - 1][y] = GP.black
            self.matrix[0][y] = GP.black

    def create_random_arena(self):       #Create random arena.
        self.create_boundaries()
        #create gray areas:
        for x in range(3):
            rand1 = (random.random() * (self.X - 1)) + 1
            rand2 = (random.random() * (self.X - 1)) + 1
            rand3 = (random.random() * (self.Y - 1)) + 1
            rand4 = (random.random() * (self.Y - 1)) + 1

            self.canvas.create_rectangle(int(min(rand1, rand2)), int(min(rand3, rand4)), int(max(rand1, rand2)),int(max(rand3, rand4)),fill='gray')
            for x in range(int(min(rand1, rand2)), int(max(rand1, rand2))):
                for y in range(int(min(rand3, rand4)), int(max(rand3, rand4))):
                    self.matrix[x][y] = GP.gray


        # create black areas:
        for x in range(1):
            rand1 = (random.random() * (self.X - 1)) + 1
            rand2 = (random.random() * (self.X - 1)) + 1
            rand3 = (random.random() * (self.Y - 1)) + 1
            rand4 = (random.random() * (self.Y - 1)) + 1

            self.canvas.create_rectangle(int(min(rand1, rand2)), int(min(rand3, rand4)), int(max(rand1, rand2)),int(max(rand3, rand4)),fill='black')
            for x in range(int(min(rand1, rand2)),int(max(rand1, rand2))):
                for y in range(int(min(rand3, rand4)), int(max(rand3, rand4))):
                    self.matrix[x][y] = GP.black

    def create_robots(self,num,isStatic):   #Create the robots.
        for x in range(num):
            self.numOfRobots=self.numOfRobots+1
            randX=0
            randY=0
            while(self.matrix[randX][randY]==GP.black): #make sure we wont put any robot on a black spot
                randX = int((random.random() * (self.X - 1)) + 1)
                randY = int((random.random() * (self.Y - 1)) + 1)
            if(isStatic):
                r = Robot.Robot(self.numOfRobots+2,isStatic,self.matrix[randX][randY],randX,randY, self.numOfMoving+self.numOfStatics)
                r.guess=[randX,randY]
                rect=self.canvas.create_rectangle(randX, randY, randX + 5, randY + 5, fill='red',tags=str(self.numOfRobots+2))
                self.robs.append([rect,self.numOfRobots+2])
                self.canvas.tag_bind(rect, '<ButtonPress-1>', self.onObjectClick)
                self.staticRob.append([r,randX,randY,rect])

            else:
                r = Robot.Robot(self.numOfRobots+2, isStatic, self.matrix[randX][randY], 0, 0,self.numOfMoving+self.numOfStatics)
                rect=self.canvas.create_rectangle(randX, randY, randX + 5, randY + 5, fill='green',tags=str(self.numOfRobots+2))
                self.robs.append([rect,self.numOfRobots+2])
                self.canvas.tag_bind(rect, '<ButtonPress-1>', self.onObjectClick)
                self.movingRob.append([r,randX,randY,rect])
            self.matrix[randX][randY] = r.id




