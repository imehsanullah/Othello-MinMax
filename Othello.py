import math
import time
from typing import Any
import turtle


class Othello:
    # Acts as Both Copy/Simple Constructor
    def __init__(self, obj=None):
        if obj is None:
            self.board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'W', 'B', ' ', ' ', ' '], [' ', ' ', ' ', 'B', 'W', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
            self.slots = 60
        else:
            self.slots = obj.slots
            self.board = [[], [], [], [], [], [], [], []]
            for i in range(0, 8):
                for j in range(0, 8):
                    if obj.board[i][j] != 'H' and obj.board[i][j] != 'C':
                        self.board[i].append(obj.board[i][j])
                    else:
                        self.board[i].append(' ')

    #Printing the Board on Console
    def Print(self):
       hpt, cpt = self.CountPoints()
       print('Human Points : ',hpt)
       print('Computer Points : ',cpt)
       print(' ',['0','1','2','3','4','5','6','7'])
       count=0
       for i in self.board:
           print(count, i)
           count=count+1

    #Putting the Disc on the Board
    def PutDisc(self,i,j,DiscColor):
        if self.board[i][j] == getPlaceWhat(DiscColor):
            self.board[i][j] = DiscColor
            self.slots-=1
            FillSlots(self,i,j)
            return True
        return False

    #Removing the Symbols from the Board which indicate the Valid Moves
    def SelfClean(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] == 'H' or self.board[i][j] == 'C':
                    self.board[i][j] = ' '

    #To Count the Discs the Computer and Human have in the Board
    def CountPoints(self):
        humanpts = 0
        Cpts = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] == 'B':
                    humanpts += 1
                elif self.board[i][j] == 'W':
                    Cpts += 1

        return humanpts, Cpts


#To check if we have Reached at the Final State in our Minmax Algo
def isLeaf(obj:Othello) -> bool:
    if obj.slots == 0:
        return True
    flag1 = CheckPossibleMoves(obj, 'B')
    obj.SelfClean()
    flag2 = CheckPossibleMoves(obj, 'W')
    obj.SelfClean()
    if flag1 == 0 and flag2 == 0:
        return True
    return False

#Evaluation Function for Othello
#e(n) = (No. Of Comp disc - No. Of Human Discs) + (2 ×No. Of Comp moves -  2× No. Of Human moves)

def Evaluationfunc(obj:Othello) -> float:
    hpts, cpts = obj.CountPoints()
    #If we have reached at the Extreme end of tree then following Calculation Takes Place
    if obj.slots == 0:
        if cpts > hpts:
            return math.inf
        elif cpts < hpts:
            return -math.inf
        elif cpts == hpts:
            return 0

    flag1 = CheckPossibleMoves(obj, 'B')
    obj.SelfClean()
    flag2 = CheckPossibleMoves(obj, 'W')
    obj.SelfClean()
    return (cpts-hpts) + (2 * flag2 - 2 * flag1)
    #No. of moves has twice the importance of No. of Discs

#The MinMax Algorithm (with alpha beta pruning) for the Problem
def minmax(obj:Othello, depth:int, isMax : bool,alpha,beta) -> float:
    if depth == 0 or isLeaf(obj):
        return Evaluationfunc(obj)
    elif isMax:
        max = -math.inf
        CheckPossibleMoves(obj, 'W')
        for i in range(0, 8):
            for j in range(0, 8):
                if obj.board[i][j] == getPlaceWhat('W'):
                    newobj = Othello(obj)
                    newobj.board[i][j] = getPlaceWhat('W')
                    newobj.PutDisc(i, j, 'W')
                    tempval = minmax(newobj, depth-1, not isMax, alpha, beta)

                    if tempval > max:
                        max = tempval
                    del newobj
                    if max > alpha:
                        alpha = max
                    if beta <= alpha:
                        break

        return max
    elif not isMax:
        min = math.inf
        CheckPossibleMoves(obj,'B')
        for i in range(0, 8):
            for j in range(0, 8):
                if obj.board[i][j] == getPlaceWhat('B'):
                    newobj = Othello(obj)
                    newobj.board[i][j]=getPlaceWhat('B')
                    newobj.PutDisc(i, j,'B')
                    tempval = minmax(newobj, depth-1, not isMax,alpha,beta)
                    if tempval < min:
                        min = tempval
                    del newobj

                    if min < beta:
                        beta = min
                    if beta <= alpha:
                        break
        return min


#To Play the Move for the Computer
def CalculatePosition(obj:Othello):
    maxI, maxJ = -1, -1
    bestGuess = -math.inf
    moves=CheckPossibleMoves(obj,'W')
    if moves !=0:
        for i in range(0, 8):
            for j in range(0, 8):
                if obj.board[i][j] == getPlaceWhat('W'):
                    newobj = Othello(obj)
                    newobj.board[i][j] = getPlaceWhat('W')
                    newobj.PutDisc(i, j, 'W')
                    branchval = minmax(newobj, 2, False,-math.inf,math.inf)
                    if bestGuess < branchval:
                        bestGuess = branchval
                        maxI ,maxJ= i, j

                    del newobj


    if maxI !=-1 and maxJ!=-1:
        obj.PutDisc(maxI, maxJ, 'W')
    obj.SelfClean()
    return maxI,maxJ

#Some Helping Functions (Ignore)
def getreverse(str):
    if str == 'B':
        return 'W'
    elif str == 'W':
        return 'B'


def getPlaceWhat(str):
    if str == 'B':
        return 'H'
    elif str == 'W':
        return 'C'


#To check the Possible Moves for a Player
def CheckPossibleMoves(obj, checkfor):

    flag=0
    for i in range(0, 8):
        for j in range(0, 8):
            # Right
            if j <= 5:
                if obj.board[i][j] == checkfor and obj.board[i][j] == getreverse(obj.board[i][ j +1]):
                    for k in range( j +1, 8):
                        if obj.board[i][k] !=getreverse(obj.board[i][j]) and obj.board[i][k ]==' ':
                            obj.board[i][k] = getPlaceWhat(checkfor)
                            flag += 1
                            break
                        if obj.board[i][k] == obj.board[i][j] or obj.board[i][k] == getPlaceWhat(checkfor) or obj.board[i][k] !=getreverse(obj.board[i][j]):
                            break
            # Down
            if i <= 5:
                if obj.board[i][j] == checkfor and obj.board[i][j] == getreverse(obj.board[ i +1][j]):
                    for k in range( i +1, 8):
                        if obj.board[k][j] !=getreverse(obj.board[i][j]) and obj.board[k][j ]==' ':
                            obj.board[k][j] = getPlaceWhat(checkfor)
                            flag += 1
                            break
                        if obj.board[k][j] == obj.board[i][j] or obj.board[k][j] ==getPlaceWhat(checkfor) or obj.board[k][j] !=getreverse(obj.board[i][j]):
                            break
            # Left
            if j >=2 :
                if obj.board[i][j] == checkfor and obj.board[i][j] == getreverse(obj.board[i][ j -1]):
                    for k in range( j -1, -1, -1):
                        if obj.board[i][k] != getreverse(obj.board[i][j]) and obj.board[i][k ]==' ':
                            obj.board[i][k ] = getPlaceWhat(checkfor)
                            flag += 1
                            break
                        if obj.board[i][k] == obj.board[i][j] or obj.board[i][k] ==getPlaceWhat(checkfor) or obj.board[i][k] != getreverse(obj.board[i][j]):
                            break
            # Up
            if i >= 2:
                if obj.board[i][j] == checkfor and obj.board[i][j] == getreverse(obj.board[i -1][j]):
                    for k in range( i -1, -1 ,-1):
                        if obj.board[k][j] !=getreverse(obj.board[i][j]) and obj.board[k][j ]==' ':
                            obj.board[k][j ]= getPlaceWhat(checkfor)
                            flag += 1
                            break
                        if obj.board[k][j] == obj.board[i][j] or obj.board[k][j] ==getPlaceWhat(checkfor) or obj.board[k][j] !=getreverse(obj.board[i][j]):
                            break
            # RightUpDiagonal
            if i>= 2 and j <=5:
                if obj.board[i][j] == checkfor and obj.board[i][j] == getreverse(obj.board[i - 1][j + 1]):
                    for l, k in zip(range(i - 1, -1, -1), range(j + 1, 8)):
                        if obj.board[l][k] != getreverse(obj.board[i][j]) and obj.board[l][k] == ' ':
                            obj.board[l][k] = getPlaceWhat(checkfor)
                            flag += 1
                            break
                        if obj.board[l][k] == obj.board[i][j] or obj.board[l][k] == getPlaceWhat(checkfor) or obj.board[l][k] != getreverse(obj.board[i][j]):
                            break
            # RightDownDiagonal
            if i <= 5 and j<=5:
                if obj.board[i][j] == checkfor and obj.board[i][j] == getreverse(obj.board[i + 1][j + 1]):
                    for l, k in zip(range(i + 1, 8), range(j + 1, 8)):
                        if obj.board[l][k] != getreverse(obj.board[i][j]) and obj.board[l][k] == ' ':
                            obj.board[l][k] = getPlaceWhat(checkfor)
                            flag += 1
                            break
                        if obj.board[l][k] == obj.board[i][j] or obj.board[l][k] == getPlaceWhat(checkfor) or obj.board[l][k] != getreverse(obj.board[i][j]):
                            break
            # LeftUpDiagonal
            if i>= 2 and j >=2:
                if obj.board[i][j] == checkfor and obj.board[i][j] == getreverse(obj.board[i - 1][j - 1]):
                    for l, k in zip(range(i - 1, -1, -1), range(j - 1, -1, -1)):
                        if obj.board[l][k] != getreverse(obj.board[i][j]) and obj.board[l][k] == ' ':
                            obj.board[l][k] = getPlaceWhat(checkfor)
                            flag += 1
                            break
                        if obj.board[l][k] == obj.board[i][j] or obj.board[l][k] == getPlaceWhat(checkfor) or obj.board[l][k] != getreverse(obj.board[i][j]):
                            break
            # LeftDownDiagonal
            if j >=2 and i<=5:
                if obj.board[i][j] == checkfor and obj.board[i][j] == getreverse(obj.board[i + 1][j - 1]):
                    for l, k in zip(range(i + 1, 8), range(j - 1, -1, -1)):
                        if obj.board[l][k] != getreverse(obj.board[i][j]) and obj.board[l][k] == ' ':
                            obj.board[l][k] = getPlaceWhat(checkfor)
                            flag += 1
                            break
                        if obj.board[l][k] == obj.board[i][j] or obj.board[l][k] == getPlaceWhat(checkfor) or obj.board[l][k] != getreverse(obj.board[i][j]):
                            break


    return flag


#To fill the SLots or reverse the Discs when you have Played the Move
def FillSlots(obj:Othello, i:int, j:int):
    #Right
    if j <= 5:
        if obj.board[i][j] == getreverse(obj.board[i][j + 1]):
            flag=False
            r=-9
            for k in range(j + 1, 8):
                if obj.board[i][k]==getreverse(obj.board[i][j]):
                    pass
                elif obj.board[i][k] == obj.board[i][j]:
                    flag=True
                    r=k
                    break
                elif obj.board[i][k] == ' ':
                    break
            if flag:
                for k in range(j + 1, r):
                    obj.board[i][k]=obj.board[i][j]
    #Left
    if j >= 2:
        if obj.board[i][j] == getreverse(obj.board[i][j - 1]):
            flag=False
            r=-9
            for k in range(j - 1, -1, -1):
                if obj.board[i][k]==getreverse(obj.board[i][j]):
                    pass
                elif  obj.board[i][k] == obj.board[i][j]:
                    flag=True
                    r=k
                    break
                elif obj.board[i][k] == ' ':
                    break
            if flag:
                for k in range(j - 1, r, -1):
                    obj.board[i][k]=obj.board[i][j]
    #UP
    if i >= 2:
        if obj.board[i][j] == getreverse(obj.board[i-1][j]):
            flag=False
            r=-9
            for k in range(i - 1, -1, -1):
                if obj.board[k][j]==getreverse(obj.board[i][j]):
                    pass
                elif  obj.board[k][j] == obj.board[i][j]:
                    flag=True
                    r=k
                    break
                elif obj.board[k][j] == ' ':
                    break
            if flag:
                for k in range(i - 1, r, -1):
                    obj.board[k][j]=obj.board[i][j]

    #Down
    if i <= 5:
        if obj.board[i][j] == getreverse(obj.board[i+1][j]):
            flag=False
            r=-9
            for k in range(i + 1, 8):
                if obj.board[k][j]==getreverse(obj.board[i][j]):
                    pass
                elif  obj.board[k][j] == obj.board[i][j]:
                    flag=True
                    r=k
                    break
                elif obj.board[k][j] == ' ':
                    break
            if flag:
                for k in range(i + 1, r):
                    obj.board[k][j]=obj.board[i][j]

    #RightupDiagonal
    if i >= 2 and j<=5:
        if obj.board[i][j] == getreverse(obj.board[i-1][j+1]):
            flag=False
            r=-9
            c=-9
            for l,k in zip(range(i - 1, -1,-1), range(j+1, 8)):
                if obj.board[l][k]==getreverse(obj.board[i][j]):
                    pass
                elif obj.board[l][k] == obj.board[i][j]:
                    flag=True
                    r=l
                    c=k
                    break
                elif obj.board[l][k] == ' ':
                    break
            if flag:
                for l,k in zip(range(i - 1, r,-1), range(j+1, c)):
                    obj.board[l][k]=obj.board[i][j]

    #RightDownDiagonal
    if i <= 5 and j<=5:
        if obj.board[i][j] == getreverse(obj.board[i+1][j+1]):
            flag=False
            r=-9
            c=-9
            for l,k in zip(range(i + 1, 8), range(j+1, 8)):
                if obj.board[l][k]==getreverse(obj.board[i][j]):
                    pass
                elif obj.board[l][k] == obj.board[i][j]:
                    flag=True
                    r=l
                    c=k
                    break

                elif obj.board[l][k] == ' ':
                    break
            if flag:
                for l,k in zip(range(i + 1, r), range(j+1, c)):
                    obj.board[l][k]=obj.board[i][j]

    #LeftupDiagonal
    if i >= 2 and j>=2:
        if obj.board[i][j] == getreverse(obj.board[i-1][j-1]):
            flag=False
            r=-9
            c=-9
            for l,k in zip(range(i - 1, -1,-1), range(j-1, -1,-1)):
                if obj.board[l][k]==getreverse(obj.board[i][j]):
                    pass
                elif obj.board[l][k] == obj.board[i][j]:
                    flag=True
                    r=l
                    c=k
                    break
                elif obj.board[l][k] == ' ':
                    break
            if flag:
                for l,k in zip(range(i - 1, r,-1), range(j-1, c,-1)):
                    obj.board[l][k]=obj.board[i][j]
    #leftdownDiagonal
    if i <= 5 and j>=2:
        if obj.board[i][j] == getreverse(obj.board[i+1][j-1]):
            flag=False
            r=-9
            c=-9
            for l,k in zip(range(i + 1, 8), range(j-1, -1,-1)):
                if obj.board[l][k]==getreverse(obj.board[i][j]):
                    pass
                elif obj.board[l][k] == obj.board[i][j]:
                    flag=True
                    r=l
                    c=k
                    break
                elif obj.board[l][k] == ' ':
                    break
            if flag:
                for l,k in zip(range(i + 1, r), range(j-1, c,-1)):
                    obj.board[l][k]=obj.board[i][j]


def getcolor(str):
    if str=='B':
        return 'black'
    elif str=='W':
        return 'White'
    elif str=='H' or str=='C':
        return 'green'



def DrawCircle(tur:turtle,i:int,j:int,str):

    tur.begin_fill()
    tur.goto(i+25, j-42)
    tur.pendown()
    tur.width(3)
    tur.circle(17)

    tur.fillcolor(getcolor(str))
    tur.end_fill()
    tur.penup()

# A function to Draw the Othello on the Turtle Screen
def DrawBoard(tur:turtle, obj:Othello):
    tur.clear()
    board: list[list[Any]] = obj.board

    hpts,cpts=obj.CountPoints()
    tur.goto(-180 , 250)
    tur.pendown()
    tur.width(5)
    tur.write(f' Human Score: {hpts}  Computer Score: {cpts}', font=("Times New Roman", 15, "bold"))
    tur.penup()

    for p in range(0, 8):
        tur.goto(-180 + p * 50, 210)
        tur.pendown()
        tur.width(5)
        tur.write(str(p), font=("Times New Roman", 15, "bold"))
        tur.penup()


    tur.goto(-220 , 170)
    tur.pendown()
    tur.width(5)
    tur.write(str(0), font=("Times New Roman", 15, "bold"))
    tur.penup()



    # First Row
    for p in range(0, 8):
        tur.begin_fill()
        tur.goto(-200 + p * 50, 200)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor('green')
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

        if board[0][p] != ' ':
            DrawCircle(tur, -200 + p * 50, 200, board[0][p])




    tur.goto(-220, 120)
    tur.pendown()
    tur.width(5)
    tur.write(str(1), font=("Times New Roman", 15, "bold"))
    tur.penup()

    # Second Row
    for p in range(0, 8):
        tur.begin_fill()
        tur.goto(-200 + p * 50, 150)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor('green')
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

        if board[1][p] != ' ':
            DrawCircle(tur, -200 + p * 50, 150, board[1][p])


    tur.goto(-220, 70)
    tur.pendown()
    tur.width(5)
    tur.write(str(2), font=("Times New Roman", 15, "bold"))
    tur.penup()
    # 3rd Row
    for p in range(0, 8):
        tur.begin_fill()
        tur.goto(-200 + p * 50, 100)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor('green')
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

        if board[2][p] != ' ':
            DrawCircle(tur, -200 + p * 50, 100, board[2][p])

    tur.goto(-220, 20)
    tur.pendown()
    tur.width(5)
    tur.write(str(3), font=("Times New Roman", 15, "bold"))
    tur.penup()

    # 4th Row
    for p in range(0, 8):
        tur.begin_fill()
        tur.goto(-200 + p * 50, 50)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor('green')
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

        if board[3][p] != ' ':
            DrawCircle(tur, -200 + p * 50, 50, board[3][p])

    tur.goto(-220, -30)
    tur.pendown()
    tur.width(5)
    tur.write(str(4), font=("Times New Roman", 15, "bold"))
    tur.penup()
    # 5th Row
    for p in range(0, 8):
        tur.begin_fill()
        tur.goto(-200 + p * 50, 0)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor('green')
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

        if board[4][p] != ' ':
            DrawCircle(tur, -200 + p * 50, 0, board[4][p])

    tur.goto(-220, -80)
    tur.pendown()
    tur.width(5)
    tur.write(str(5), font=("Times New Roman", 15, "bold"))
    tur.penup()

    # 6th Row
    for p in range(0, 8):
        tur.begin_fill()
        tur.goto(-200 + p * 50, -50)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor('green')
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

        if board[5][p] != ' ':
            DrawCircle(tur, -200 + p * 50, -50, board[5][p])

    tur.goto(-220, -130)
    tur.pendown()
    tur.width(5)
    tur.write(str(6), font=("Times New Roman", 15, "bold"))
    tur.penup()

    # 7th Row
    for p in range(0, 8):
        tur.begin_fill()
        tur.goto(-200 + p * 50, -100)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor('green')
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

        if board[6][p] != ' ':
            DrawCircle(tur, -200 + p * 50, -100, board[6][p])


    tur.goto(-220, -180)
    tur.pendown()
    tur.width(5)
    tur.write(str(7), font=("Times New Roman", 15, "bold"))
    tur.penup()

    # 8th Row
    for p in range(0, 8):
        tur.begin_fill()
        tur.goto(-200 + p * 50, -150)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor('green')
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

        if board[7][p] != ' ':
            DrawCircle(tur, -200 + p * 50, -150, board[7][p])




""""""

if __name__ == '__main__':

    #Initialising Turtles Variables for the Graphical Representation of the Othello
    a = turtle.Screen()
    a.bgcolor('green')
    turtle.delay(0)
    tur = turtle.Turtle()

    tur.hideturtle()
    tur.penup()
    tur.speed(0)

    obj = Othello()
    state = 'B'

    flag=False

    Ci=-1
    Cj=-1
    while isLeaf(obj)==False:
        if state == 'B':
            moves = CheckPossibleMoves(obj, state)
            if moves != 0:
                obj.Print()
                DrawBoard(tur,obj)
                if Ci !=-1 and Cj!=-1:
                    tur.goto(-180, -250)
                    tur.pendown()
                    tur.width(5)
                    tur.write(f'The Last Move by Computer was i : {Ci}  j: {Cj}',font=("Times New Roman", 15, "bold"))
                    tur.penup()
                Ci = -1
                Cj = -1

                flag=False
                i = int(input('Enter i: '))
                j = int(input('Enter j: '))
                if obj.board[i][j] != getPlaceWhat(state):
                    tur.goto(-300, -275)
                    tur.pendown()
                    tur.width(5)

                    tur.write(f'You Entered Invalid Co-ordinates i : {i}  j: {j} move is not allowed', font=("Times New Roman", 15, "bold"))
                    tur.penup()
                    time.sleep(2)
                    print('Wrong i/p')
                else:
                    obj.PutDisc(i,j,state)
                    state = getreverse(state)
                    obj.SelfClean()
            else:
                state = getreverse(state)
                tur.goto(-180, -250)
                tur.pendown()
                tur.width(5)
                tur.write(' You do not have any Valid Move , So the Computer will make it move', font=("Times New Roman", 15, "bold"))
                tur.penup()
                time.sleep(2)
                flag = True

        elif state == 'W':
            Ci,Cj=CalculatePosition(obj)
            state = getreverse(state)
            if flag:
                DrawBoard(tur, obj)
                time.sleep(2)


    DrawBoard(tur,obj)
    hpts, cpts=obj.CountPoints()
    msg='None'
    if hpts > cpts:
        msg = 'Congrats you Won'
    elif hpts < cpts:
        msg = 'Oho the Computer Won this Round'
    elif hpts == cpts:
        msg = 'The Match is a Tie b/w both'

    tur.goto(-180, -250)
    tur.pendown()
    tur.width(5)
    tur.write(msg, font=("Times New Roman", 15, "bold"))
    tur.penup()

    print('Click on the Turtle Window to close it')
    turtle.exitonclick()
"""    """
