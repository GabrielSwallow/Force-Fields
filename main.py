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

params = {
    "axes.labelsize":16,
    "font.size":20,
    "legend.fontsize":30,
    "xtick.labelsize":20,
    "ytick.labelsize":20,
    "figure.figsize": [15,15],
}
plt.rcParams.update(params)

fig, axs = plt.subplots(1,1)
camera = Camera(fig)

axis = 5
arrows = 50
times = np.linspace(0,60,3000)

p1 = -3
p2 = 3

def force(r):
    x,y = r[0], r[1]
    
    u = -(x-p1) * 1/((x-p1)**2 + y**2)
    v = -y/((x-p1)**2 + y**2)
    
    u+= -(x-p2)*1/((x-p2)**2 + y**2)
    v+= -y*1/((x-p2)**2 + y**2)
    
    return [u,v]
    

    

ball = objects.ball(1, 1, [0,0], [0.7,1])
ball.propagate_system(force, times)



x,y = np.meshgrid(np.linspace(-axis,axis,arrows),
                  np.linspace(-axis,axis,arrows))

u = -(x-p1) * 1/((x-p1)**2 + y**2)
v = -y/((x-p1)**2 + y**2)
    
u+= -(x-p2)*1/((x-p2)**2 + y**2)
v+= -y*1/((x-p2)**2 + y**2)

#q = plt.quiver(x,y,u,v, units='width')
#plt.quiverkey(q, X=0.3, Y=0.3, U=10, label='Quiver key, length = 10', labelpos='E')
#plt.show()

#plt.quiver(x,y,u,v, units='width')

#only one can be True
OG = False
if OG:
    plt.plot(ball.positions[0][:,0], ball.positions[0][:,1], linewidth=5)
    q = plt.quiver(x,y,u,v, units='width')
    #plt.quiverkey(q, X=0.3, Y=0.3, U=10, label='Quiver key, length = 10', labelpos='E')
    plt.show()


animation = True
tail_factor = 8
tail = tail_factor*5
axes_lim = 6

if animation:
    alphas = np.linspace(0.1, 1, tail)
    alphas = np.array([i**2 for i in np.linspace(0.1, 1, tail)])
    rgba_colors = np.zeros((tail,4))
    # for red the first column needs to be one
    rgba_colors[:,0] = 1.0
    # the fourth column needs to be the alphas
    rgba_colors[:, 3] = alphas

    for t in range(int(len(times)/5)):
        rx, ry = ball.velocities[0][:,0][t], ball.positions[0][:,1][t]
        #vx, vy = ball.velocities[0][:,0][t], ball.positions[0][:,1][t]
        plt.plot(p1,0, 'o', ms=30, mew=15, color='b')
        plt.plot(p2,0, 'o', ms=30, mew=15, color='b')
        plt.scatter(ball.positions[0][(t-tail_factor)*5:(t)*5,0], 
                 ball.positions[0][(t-tail_factor)*5:t*5,1], 
                 color=rgba_colors[0:len(ball.positions[0][(t-tail_factor)*5:(t)*5,0])])
        #plt.plot(ball.positions[0][(t-4)*5:t*5,0], 
                # ball.positions[0][(t-4)*5:t*5,1], 
                # linewidth=5, color='r')
        plt.plot(ball.positions[0][t*5,0],ball.positions[0][t*5,1],
                 'o', ms=10, mew=3, color='r')
        axs.set_title('Two planets, one orbiting object')
        #axs.plot(rx, ry, 'o', color='r', mew=10)
        axs.grid(True)
        axs.set_xlim(-axes_lim,axes_lim)
        axs.set_ylim(-axes_lim,axes_lim)
    
        #print(t)
        camera.snap()
    
    anim = camera.animate()
    pillow = PillowWriter(fps=45)
    filename = directory + "\\Animation.gif" 
    anim.save(filename, writer=pillow)
    
    