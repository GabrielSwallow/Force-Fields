# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 13:47:15 2021

@author: gabri
"""

import numpy as np
from scipy.integrate import odeint


class ball:
    def __init__(self, mass, radius, pos, v):
        self.initial_pos = pos
        self.initial_v = v
        self.v=v
        self.pos = pos
        self.mass = mass
        self.radius = radius
        self.volume = (4*np.pi*radius**3)/(3)
        self.positions = []
        self.velocities = []
    
    def propagate_system(self, force, times):
        def ODEs(variables, times):
            r, v = variables[0:2], variables[2::]
            dv_dt = [force(r)[0]/self.mass , force(r)[1]/self.mass]
            dr_dt = v
          
            return np.append(dr_dt, dv_dt)
        initial_conditions = self.initial_pos + self.initial_v
        solution = odeint(ODEs , initial_conditions , times)
        self.positions.append(solution[:,0:2])
        self.velocities.append(solution[:,2::])