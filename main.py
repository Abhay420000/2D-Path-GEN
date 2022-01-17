from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.instructions import InstructionGroup
from kivy.core.window import Window
from kivy.graphics import Line
import random

class BBG(Widget):
    def __init__(self):
        super().__init__()
        
        self.pth = InstructionGroup()
        self.w = 2#Path Segments' width
        
        number_of_lines_in_path = random.randint(5,50)#Generating Random Amount Of Lines
        #print(number_of_lines_in_path)

        self.div = int(Window.size[0]/number_of_lines_in_path)#Dividing Equal Sized Paths
        px = 0
        py = random.randint(int(Window.size[1]/3), int(Window.size[1]/2))
        
        for i in range(0, number_of_lines_in_path+100):
                        #Adding 100 in case if all line's(path segment's) become less
                        #than length of x-axis because of all line's length may differ due to angle.
            pline = Line(points = [px,py,px+self.div,random.randint(int(Window.size[1]/3), int(Window.size[1]/2))], width = self.w)
            self.pth.add(pline)
            px = pline.points[2]
            py = pline.points[3]
                        
        self.canvas.add(self.pth)
        Clock.schedule_interval(self.animate_path, 0.01)

    def animate_path(self, _utk):
        #For Movement of all Path's Segments
        for i in range(0,self.pth.length()):
            if (type(self.pth.children[i]) == type(Line())):
                if (self.pth.children[i].points[2] != 0):
                    newL = self.pth.children[i]
                    p = self.pth.children[i].points
                    p[0] -= 1
                    p[2] -= 1
                    self.pth.insert(i, Line(points = p, width = self.w))
                    self.pth.remove(newL)

        #Removing a path's segment when it leaves the screen
        for i in range(0,self.pth.length()):
            if (type(self.pth.children[i]) == type(Line())):
                if (self.pth.children[i].points[2] <= 0):
                    newL = self.pth.children[i]
                    length = self.pth.children[i].points[2] - self.pth.children[i].points[0]
                    self.pth.remove(newL)
                    self.make_path(length)
                    break
    
    def make_path(self,length):
        """
        For Adding new Lines(Path Segment)
        """
        px = 0
        for i in range(self.pth.length()-1,-1,-1):
            if (type(Line()) == type(self.pth.children[i])):
                px = self.pth.children[i].points[2]
                py = self.pth.children[i].points[3]
                break
            
        ny = random.randint(int(Window.size[1]/3), int(Window.size[1]/2))
        newLine = Line(points = [px,py,px+length,ny], width = self.w)
        self.pth.add(newLine)
            

class BBApp(App):
    def build(self):
        return BBG()

if __name__ == '__main__':
    BBApp().run()
