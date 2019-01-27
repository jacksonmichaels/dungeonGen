from graphics import *
import os
import random
#for Dir True = vertical False = horizontal


#Constants:
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
MIN_SIZE = 50000



class Room:
    def __init__(self, tl, br):
        self.topL = tl
        self.botR = br

        self.shape = Rectangle(self.topL, self.botR)
        self.shape.setFill(color_rgb(256, 256, 256))

    def draw(self, window):
        self.shape.draw(window)

    def move(self, x, y):
        self.topL.x += x
        self.botR.x += x

        self.topL.y += y
        self.botR.y += y

        self.shape.move(x,y)

class Node:
    def __init__(self, topLeft, botRight, left = None, right = None, dir = False, room = None):
        self.tl = topLeft
        self.br = botRight

        self.left = left
        self.right = right

        self.dir = dir

        self.room = None

        self.parent = None

        self.room = room

    def getSize(self, mode = 'd'):
        wide = self.br.x - self.tl.x
        tall = self.br.y - self.tl.y

        if (mode == 'd'):
            return (wide, tall)
        else:
            return wide * tall

class BSP:
    def __init__(self, minSize, window):
        self.min = minSize
        self.win = window

        self.head = Node(Point(0, 0), Point(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.rooms = 0

    def generate(self, node):
        (wide, tall) = node.getSize()
        if (node.dir):
            left = Node(node.tl, Point(node.tl.x + int(wide/2), node.br.y), dir = not node.dir)

            right = Node(Point(node.tl.x + int(wide / 2), node.tl.y), node.br, dir = not node.dir)


        else:
            left = Node(node.tl, Point(node.br.x, node.tl.y + int(tall / 2)), dir = not node.dir)

            right = Node(Point(node.tl.x, node.tl.y + int(tall / 2)), node.br, dir = not node.dir)

        node.left = left
        node.right = right

        node.left.parent = node
        node.right.parent = node


        if (left.getSize('a') < MIN_SIZE):

            room = randRoom(left.getSize()[0], left.getSize()[1])

            room.move(left.tl.x, left.tl.y)

            room.draw(self.win)

            Rectangle(left.tl, left.br).draw(self.win)

            node.left.room = room
            self.rooms += 1

        else:
            self.generate(node.left)


        if (right.getSize('a') < MIN_SIZE):

            room = randRoom(right.getSize()[0], right.getSize()[1])

            room.move(right.tl.x, right.tl.y)

            room.draw(self.win)

            Rectangle(right.tl, right.br).draw(self.win)
            node.right.room = room
            self.rooms += 1

        else:
            self.generate(node.right)



    def connectRooms(self, node):
        if (node.left and node.right):
            self.connectRooms(node.left)
            self.connectRooms(node.right)

        else:
            node = node.parent

            lc = Point((node.left.room.topL.x + node.left.room.botR.x) / 2, (node.left.room.topL.y + node.left.room.botR.y) / 2)
            rc = Point((node.right.room.topL.x + node.right.room.botR.x) / 2, (node.right.room.topL.y + node.right.room.botR.y) / 2)

            link = Line(lc, rc)

            link.setWidth(10)

            link.draw(self.win)





def addPoints(a, b):
    ret = Point(a.x + b.x, a.y + b.y)

    return ret

def randRoom(width, height, minDem = 50):
    tl = Point(random.randrange(width - minDem), random.randrange(height - minDem))

    br = Point(random.randrange(tl.x + minDem, width), random.randrange(tl.y + minDem, height))

    room = Room(tl, br)

    return room

win = GraphWin("Game", WINDOW_WIDTH, WINDOW_HEIGHT)


tree = BSP(MIN_SIZE, win)

tree.generate(tree.head)

tree.connectRooms(tree.head)


win.getMouse()

win.close()
