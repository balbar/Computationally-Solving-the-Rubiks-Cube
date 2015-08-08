
# coding: utf-8

# <h1 align=center>Computationally Solving the Rubik's Cube <h6 />

# In[107]:

from ipythonblocks import BlockGrid
import numpy as np


# Each color pixel was represented by a color, followed by a 12x9 grid to represent a 2D Rubik's Cube. Next, a loop was created to link the matrices that were constructed later on with the grid so that the colors assigned to the arrays will also change the colors on the grid accordingly.

# In[108]:

colors = {
    1 : (0,0,0),
    2 : (0,255,0),
    3 : (250,250,10),
    4 : (0,0,255),
    5 : (255,200,0),
    6 : (256,0,0)
        }

grid = BlockGrid(12,9, fill=(256, 256, 256))

facemap = {}
for i in range(3):
    for j in range(3):
        facemap[(0,i,j)] = (6+i,3+j)
        facemap[(1,i,j)] = (5-j,6+i)
        facemap[(2,i,j)] = (2-i,5-j)
        facemap[(3,i,j)] = (3+j,2-i)
        facemap[(4,i,j)] = (3+i,3+j)
        facemap[(5,i,j)] = (5-i,11-j)


# This function takes the colors of the arrays and links them with the blocks on the grid.

# In[109]:

def newgrid(G,facemap):    
    for face, block in facemap.iteritems():
        grid[block] = colors[G[face]]
    return grid


# This dictionary assigns each element on every array, a color to represent the initial configuration.

# In[110]:

def init():
    #F = 0
    G = np.zeros((6,3,3))
    G[0,0,2] = 1
    G[0,1,2] = 1
    G[0,2,2] = 2 
    G[0,2,1] = 3  
    G[0,2,0] = 6 
    G[0,1,1] = 1
    G[0,1,0] = 5
    G[0,0,0] = 1
    G[0,0,1] = 5

    #R = 1
    G[1,0,2] = 4
    G[1,1,2] = 6
    G[1,2,2] = 5
    G[1,2,1] = 5
    G[1,1,1] = 4
    G[1,2,0] = 5
    G[1,1,0] = 2
    G[1,0,0] = 2
    G[1,0,1] = 3

    #B = 2
    G[2,0,2] = 4
    G[2,1,2] = 4
    G[2,2,2] = 5
    G[2,2,1] = 1
    G[2,1,1] = 3
    G[2,2,0] = 3
    G[2,1,0] = 4
    G[2,0,0] = 6
    G[2,0,1] = 6

    #L = 3
    G[3,0,2] = 5
    G[3,1,2] = 2
    G[3,2,2] = 2
    G[3,2,1] = 4
    G[3,1,1] = 4
    G[3,2,0] = 2
    G[3,1,0] = 3
    G[3,0,0] = 1
    G[3,0,1] = 4

    #U = 4
    G[4,0,2] = 3
    G[4,1,2] = 2
    G[4,2,2] = 6
    G[4,1,1] = 6
    G[4,2,1] = 3
    G[4,2,0] = 4
    G[4,1,0] = 1
    G[4,0,0] = 6
    G[4,0,1] = 1

    #D = 5
    G[5,0,2] = 1
    G[5,1,2] = 5
    G[5,2,2] = 4
    G[5,1,1] = 5
    G[5,2,1] = 2
    G[5,2,0] = 3
    G[5,1,0] = 6
    G[5,0,0] = 3
    G[5,0,1] = 6
    return G


# The configuration that was assigned in the previous cell is shown in this 2D grid as an example.

# In[111]:

G = init()
grid = newgrid(G,facemap)
grid


# In[116]:

def solved(): 
    G = np.zeros((6,3,3))
    G[0,:,:] = 1
    G[1,:,:] = 2
    G[2,:,:] = 3
    G[3,:,:] = 4
    G[4,:,:] = 6
    G[5,:,:] = 5
    return G


# In[117]:

G = solved()
grid = newgrid(G,facemap)
grid


# This function takes the solved state of the cube and rearranges the cubies in any random configuration.

# In[118]:

def randomconfig(X):
    import random
    scramble = ''.join(random.choice('FRLBUD') for _ in xrange(X))
    grid = newgrid(solved(),facemap)
    G = rotatecube(scramble,solved())
    return G


# In[119]:

G = randomconfig(1000)
grid = newgrid(G,facemap)
grid


# Six functions were made to represent the rotation of each face 90 degrees clockwise by transposing the arrays and multiplying them by the matrix below to get the result of a rotation. After that, the other faces that change as a result of the rotation, were also changed by replacing them with the appropriate row or column.

# In[112]:

def Frotate(G):
    GG = G.copy()
    A = np.array([[0,0,1],[0,1,0],[1,0,0]])
    GG[0,:,:] = np.dot(GG[0,:,:].T,A)

    GG[4,2,:3] = G[3,:,2]
    GG[1,:3,0] = G[4,2,:3]
    GG[5,0,:3] = G[1,:3,0]
    GG[3,:,2] = G[5,0,:3]
    return GG

def Rrotate(G): 
    GG = G.copy()
    P = np.array([[0,0,1],[0,1,0],[1,0,0]])
    GG[1,:,:] = np.dot(GG[1,:,:].T,P)

    GG[4,:,2] = G[0,:,2]
    GG[2,:,0] = G[4,:,2]
    GG[0,:,2] = G[5,:,2] 
    GG[5,:,2] = G[2,:,0]
    return GG

def Brotate(G):
    GG = G.copy()
    P = np.array([[0,0,1],[0,1,0],[1,0,0]])
    GG[2,:,:] = np.dot(GG[2,:,:].T,P)

    GG[3,:,0] = G[4,0,:3] 
    GG[5,2,:3] = G[3,:,0]
    GG[1,:3,2] = G[5,2,:3]
    GG[4,0,:3] = G[1,:3,2]
    return GG

def Lrotate(G):
    GG = G.copy()
    P = np.array([[0,0,1],[0,1,0],[1,0,0]])
    GG[3,:,:] = np.dot(GG[3,:,:].T,P)

    GG[0,:3,0] = G[4,:3,0]
    GG[5,:,0] = G[0,:3,0]
    GG[2,:3,2] = G[5,:,0]
    GG[4,:3,0] = G[2,:3,2]
    return GG

def Urotate(G):
    GG = G.copy()
    P = np.array([[0,0,1],[0,1,0],[1,0,0]])
    GG[4,:,:] = np.dot(GG[4,:,:].T,P)

    GG[3,0,:] = G[0,0,:]
    GG[2,0,:] = G[3,0,:]
    GG[1,0,:] = G[2,0,:]
    GG[0,0,:] = G[1,0,:]
    return GG

def Drotate(G):
    GG = G.copy()
    P = np.array([[0,0,1],[0,1,0],[1,0,0]])
    GG[5,:,:] = np.dot(GG[5,:,:].T,P)

    GG[0,2,:3] = G[3,2,:]
    GG[3,2,:] = G[2,2,:3]
    GG[2,2,:3] = G[1,2,:3]
    GG[1,2,:3] = G[0,2,:3]
    return GG


# Each rotation function is represented by a letter so it is easier to call on multiple rotations at once.

# In[113]:

def rotatecube(faces,G):
    for face in faces:
        if face == 'F':
            G = Frotate(G)
        if face == 'R':
            G = Rrotate(G)
        if face == 'B':
            G = Brotate(G)
        if face == 'L':
            G = Lrotate(G)
        if face == 'U':
            G = Urotate(G)
        if face == 'D':
            G = Drotate(G)
    return G


# When one white edge is in its correct place, this function rotates the cube so the next edge could be solved.

# In[79]:

def rotatewholecube(G):
    GG = G.copy()
    GG[0,:,:] = G[3,:,:]
    GG[3,:,:] = G[2,:,:]
    GG[2,:,:] = G[1,:,:]
    GG[1,:,:] = G[0,:,:]
    
    P = np.array([[0,0,1],[0,1,0],[1,0,0]])
    GG[4,:,:] = np.dot(P,GG[4,:,:].T)
    
    P = np.array([[0,0,1],[0,1,0],[1,0,0]])
    GG[5,:,:] = np.dot(P,GG[5,:,:].T)
    return GG


# This function locates all the white edges and rotates them to their correct cubies.

# In[103]:

def rotatewhite(G):
    for i in range(4):
        while G[0,2,1] != 1 and G[5,0,1] != 1:
            if (G[3,2,1] == 1 or G[5,1,0] == 1):
                G = rotatecube('D',G)
                print 'case1'
            elif (G[3,0,1] == 1 or G[4,1,0] == 1):
                G = rotatecube('FBBBLBFFF',G)
                print 'case2'
            elif (G[1,0,1] == 1 or G[4,1,2] == 1):
                G = rotatecube('FFFBRRRBBBF',G)
                print 'case3'
            elif (G[1,2,1] == 1 or G[5,1,2] == 1):
                G = rotatecube('DDD',G)
                print 'case4'
            elif (G[3,1,0] == 1 or G[2,1,2] == 1):
                G = rotatecube('RLLLDLRRR',G)
                print 'case5'
            elif (G[4,0,1] == 1 or G[2,0,1] == 1):
                G = rotatecube('BLLLRDLRRR',G)
                print 'case6'
            elif (G[1,1,2] == 1 or G[2,1,0] == 1):
                G = rotatecube('RLLLDDDLRRR',G)
                print 'case7'
            elif (G[2,2,1] == 1 or G[5,2,1] == 1):
                G = rotatecube('DD',G)
                print 'case8'
               # raw_input()
            G = rotatewholecube(G)
        return G


# If a white edge is in the correct cubie but is placed on the wrong side, this function rotates the cube to get it in its correct location.

# In[104]:

def rotatewhiteedges(G):
    for i in range(4):
        if G[5,0,1] == 1:
            rotatecube('RLLLDDDLRRRDRLLLDDRRRL',G)
        else:
            rotatewholecube(G)
        return G


# In[ ]:



