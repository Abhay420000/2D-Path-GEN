from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.instructions import InstructionGroup
from kivy.core.window import Window
from kivy.graphics import Line
from kivy.graphics import Quad
from kivy.graphics import Color
from kivy.uix.image import Image
import random

class BBG(Widget):
    def __init__(self):
        super().__init__()

        with self.canvas:
            self.bind(size = self.update_rect,)
            
        self.img = Image(source = f'{random.randint(1,2)}.jpg', pos = (0, 0), size = Window.size, allow_stretch = True, keep_ratio = False)
        self.add_widget(self.img)
        self.img.bind(size = self.update_rect,)
   
        self.pth = InstructionGroup()
        self.w = 4#Path Segments'(Grass,Line) width
        self.step = 5
        
        number_of_lines_in_path = random.randint(5,50)#Generating Random Amount Of Lines
        #print(number_of_lines_in_path)

        self.div = int(Window.size[0]/number_of_lines_in_path)#Dividing Equal Sized Paths
        px = -500
        py = random.randint(int(Window.size[1]/3), int(Window.size[1]/2))
        
        for i in range(0, number_of_lines_in_path+50):
                        #Adding 100 in case if all line's(path segment's) become less
                        #than length of x-axis because of all line's length may differ due to angle.
            pline = Line(points = [px,py,px+self.div,random.randint(int(Window.size[1]/3), int(Window.size[1]/2))], width = self.w, )
            qds = Quad(points = pline.points+[pline.points[2],0,pline.points[0],0])
            self.pth.add(Color(0.5,0.4,0.1,1))
            self.pth.add(qds)
            self.pth.add(Color(0,1,0,1))
            self.pth.add(pline)

            #Storing This For Connecting Next Segment to it
            px = pline.points[2]
            py = pline.points[3]

        self.canvas.add(self.pth)
        Clock.schedule_interval(self.animate_path, 0.0666)#60FPS

    def update_rect(self, *args):
        self.img.size = Window.size
    
    def animate_path(self, _utk):
        #For Movement of all Path's Segments
        for i in range(0,self.pth.length()):
            if (type(self.pth.children[i]) == type(Line())):
                if (self.pth.children[i].points[2] >= -250):
                    newL = self.pth.children[i]
                    p = self.pth.children[i].points
                    p[0] -= self.step
                    p[2] -= self.step
                    self.pth.insert(i, Line(points = p, width = self.w))
                    self.pth.remove(newL)
            if (type(self.pth.children[i]) == type(Quad())):
                if (self.pth.children[i].points[2] >= -250):
                    newL = self.pth.children[i]
                    p = self.pth.children[i].points
                    p[0] -= self.step
                    p[2] -= self.step
                    p[4] -= self.step
                    p[6] -= self.step
                    self.pth.insert(i, Quad(points = p))
                    self.pth.remove(newL)
        
        #Removing a path's segment when it leaves the screen
                
        for i in range(0,self.pth.length()):#Deleting Quad
            if (type(self.pth.children[i]) == type(Quad())):
                if (self.pth.children[i].points[2] <= -250):
                    to_delete_Quad = self.pth.children[i]
                    if (type(self.pth.children[i-1]) == type(Color())):
                        #print(1)
                        self.pth.remove(self.pth.children[i-1])
                    self.pth.remove(to_delete_Quad)
                    break
                                
        for i in range(0,self.pth.length()):#Deleting Line
            if (type(self.pth.children[i]) == type(Line())):
                if (self.pth.children[i].points[2] <= -250):
                    old_Line = self.pth.children[i]
                    length = self.pth.children[i].points[2] - self.pth.children[i].points[0]
                    if (type(self.pth.children[i-1]) == type(Color())):
                        #print(2)
                        self.pth.remove(self.pth.children[i-1])
                    self.pth.remove(old_Line)
                    self.make_path(length)#Adding new Segment
                    break

        #print(self.pth.length())
    
    def make_path(self,length):
        """
        For Adding new Road
        """
        #px = 0
        #py = random.randint(int(Window.size[1]/3), int(Window.size[1]/2))
        
        for i in range(self.pth.length()-1,-1,-1):
            if (type(self.pth.children[i]) == type(Line())):
                px = self.pth.children[i].points[2]
                py = self.pth.children[i].points[3]
                break
            
        ny = random.randint(int(Window.size[1]/3), int(Window.size[1]/2))

        newLine = Line(points = [px,py,px+length,ny], width = self.w)
        qds = Quad(points = newLine.points+[newLine.points[2],0,newLine.points[0],0])

        self.pth.add(Color(0.5,0.4,0.1))
        self.pth.add(qds)
        self.pth.add(Color(0,1,0))
        self.pth.add(newLine)

class BBApp(App):
    def build(self):
        return BBG()

if __name__ == '__main__':
    BBApp().run()
