# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 13:46:04 2021

I think the animation isn't working because the solver does more work, and 
makes more plots of position between each time step

@author: gabri
"""
from importlib import reload  
import numpy as np
import matplotlib.pyplot as plt
import objects
import os
from matplotlib.animation import PillowWriter
from celluloid import Camera
reload(objects)

directory = os.path.dirname(os.path.realpath(objects.__file__))

fig, axs = plt.subplots(1,1)
camera = Camera(fig)

params = {
    "axes.labelsize":16,
    "font.size":20,
    "legend.fontsize":30,
    "xtick.labelsize":20,
    "ytick.labelsize":20,
    "figure.figsize": [15,15],
}
plt.rcParams.update(params)

axis = 5
arrows = 50
times = np.linspace(0,60,500)


def force(r):
    x,y = r[0], r[1]
    
    u = -x * 1/(x**2 + y**2)
    v = -y/(x**2 + y**2)
    
    return [u,v]
    

    

ball = objects.ball(1, 1, [2,0], [0,1.1])
ball.propagate_system(force, times)



x,y = np.meshgrid(np.linspace(-axis,axis,arrows),
                  np.linspace(-axis,axis,arrows))

u = -x/(x**2 + y**2)
v = -y/(x**2 + y**2)

#q = plt.quiver(x,y,u,v, units='width')
#plt.quiverkey(q, X=0.3, Y=0.3, U=10, label='Quiver key, length = 10', labelpos='E')
#plt.show()

#plt.quiver(x,y,u,v, units='width')


OG = True
if OG:
    plt.plot(ball.positions[0][:,0], ball.positions[0][:,1], linewidth=5)
    q = plt.quiver(x,y,u,v, units='width')
    #plt.quiverkey(q, X=0.3, Y=0.3, U=10, label='Quiver key, length = 10', labelpos='E')
    plt.show()


animation = False
if animation:

    for t in range(len(times)):
        rx, ry = ball.velocities[0][:,0][t], ball.positions[0][:,1][t]
        #vx, vy = ball.velocities[0][:,0][t], ball.positions[0][:,1][t]
        axs.plot(rx, ry, 'o', color='r', mew=10)
        axs.grid(True)
        axs.set_xlim(-5,5)
        axs.set_ylim(-5,5)
    
        
        camera.snap()
    
    anim = camera.animate()
    pillow = PillowWriter(fps=25)
    filename = directory + "\\Animation.gif" 
    anim.save(filename, writer=pillow)