from graphics import *
import os
import random
import sys
#for Dir True = vertical False = horizontal


#Constants:
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
MIN_SIZE = 100
DRAW_GRID = False
PATH_WIDTH = MIN_SIZE / 25
COLORFUL = False



class Room:
    def __init__(self, tl, br):
        self.topL = tl
        self.botR = br

        self.shape = Rectangle(self.topL, self.botR)

        if (COLORFUL):
            self.color = color_rgb(random.randrange(255),random.randrange(255),random.randrange(255))
        else:
            self.color = color_rgb(0,0,0)

        self.shape.setFill(self.color)

    def draw(self, window):
        self.shape.draw(window)

    def move(self, x, y):
        self.topL.x += x
        self.botR.x += x

        self.topL.y += y
        self.botR.y += y

        self.shape.move(x,y)

    def getCenter(self):
        return Point((self.topL.x + self.botR.x)/2, (self.topL.y + self.botR.y)/2)

class Node:
    def __init__(self, topLeft, botRight, left = None, right = None, dir = False, room = None, id=""):
        self.tl = topLeft
        self.br = botRight

        self.left = left
        self.right = right

        self.dir = dir

        self.room = None

        self.parent = None

        self.room = room

        self.childRooms = []
        self.id = id

        self.text = Text(Point(self.tl.x + 50, self.tl.y + 20), id)

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

        self.head = Node(Point(0, 0), Point(WINDOW_WIDTH, WINDOW_HEIGHT), id = "")

        self.rooms = 0


    def makeMap(self):
        self.generate(self.head)

        self.makeRoomList(self.head)

        self.connectRooms(self.head)

    def generate(self, node):
        (wide, tall) = node.getSize()
        if (node.dir):

            line = int(random.randrange(0, wide) * 0.4 + wide * 0.3)

            left = Node(node.tl, Point(node.tl.x + line, node.br.y), dir = not node.dir, id = node.id + 'L ')

            right = Node(Point(node.tl.x + line, node.tl.y), node.br, dir = not node.dir,  id = node.id + 'R ')


        else:

            line = int(random.randrange(0, tall) * 0.4 + tall * 0.3)

            left = Node(node.tl, Point(node.br.x, node.tl.y + line), dir = not node.dir,  id = node.id + 'L ')

            right = Node(Point(node.tl.x, node.tl.y + line), node.br, dir = not node.dir,  id = node.id + 'R ')


        node.left = left
        node.right = right

        node.left.parent = node
        node.right.parent = node



        if (min(left.getSize()[0], left.getSize()[1]) < MIN_SIZE):

            room = randRoom(left.getSize()[0], left.getSize()[1])

            room.move(left.tl.x, left.tl.y)

            room.draw(self.win)


            if (DRAW_GRID):
                Rectangle(node.left.tl, node.left.br).draw(self.win)

            node.left.room = room
            self.rooms += 1

        else:
            self.generate(node.left)


        if (min(right.getSize()[0], right.getSize()[1]) < MIN_SIZE):

            room = randRoom(right.getSize()[0], right.getSize()[1])

            room.move(right.tl.x, right.tl.y)

            room.draw(self.win)


            if (DRAW_GRID):
                Rectangle(node.right.tl, node.right.br).draw(self.win)


            node.right.room = room
            self.rooms += 1

        else:
            self.generate(node.right)


    def makeRoomList(self, node):
        if (node.room):
            node.childRooms.append(node.room)

        if (node.left):
            node.childRooms += self.makeRoomList(node.left)
        if (node.right):
            node.childRooms += self.makeRoomList(node.right)

        return node.childRooms


    def connectRooms(self, node):
        if (node.left):
            self.connectRooms(node.left)

        if (node.right):
            self.connectRooms(node.right)

        if (node.left and node.right):

            pair = self.closestRooms(node.left.childRooms, node.right.childRooms)

            link = Line(pair[0].getCenter(), pair[1].getCenter())
            midPoint = link.getCenter()

            if (COLORFUL):
                line1 = Line(pair[0].getCenter(), midPoint)
                line2 = Line(midPoint, pair[1].getCenter())

                line1.setFill(pair[0].color)
                line2.setFill(pair[1].color)

                line1.setWidth(PATH_WIDTH)
                line2.setWidth(PATH_WIDTH)

                line1.draw(self.win)
                line2.draw(self.win)
            else:
                link.setWidth(PATH_WIDTH)
                link.draw(self.win)

            node.childRooms.append(Room(midPoint,midPoint))


    def closestRooms(self, aRooms, bRooms):
        minDist = max(WINDOW_WIDTH, WINDOW_HEIGHT)
        minPair = None

        for aRoom in aRooms:
            for bRoom in bRooms:
                dist = getDist(aRoom.getCenter(), bRoom.getCenter())
                if (dist < minDist):
                    minDist = dist
                    minPair = (aRoom, bRoom)

        return minPair

def getDist(pointA, pointB):
    xdif = (pointA.x - pointB.x)**2
    ydif = (pointA.y - pointB.y)**2

    hyp = (xdif + ydif)**0.5

    return hyp

def addPoints(a, b):
    ret = Point(a.x + b.x, a.y + b.y)

    return ret

def randRoom(width, height):
    minDem = int(min(width, height) / 2)
    tl = Point(random.randrange(width - minDem), random.randrange(height - minDem))

    br = Point(random.randrange(tl.x + minDem, width), random.randrange(tl.y + minDem, height))

    room = Room(tl, br)

    return room

win = GraphWin("Game", WINDOW_WIDTH, WINDOW_HEIGHT)
if (COLORFUL):
    win.setBackground(color_rgb(0,0,0))

tree = BSP(MIN_SIZE, win)

tree.makeMap()

win.getMouse()

win.close()
