import numpy as np
from pylab import *

'''
here:
q_BO = [qs qv(in body frame)]
dt is time step
W,B are in body frame

the code assumes: 
q_BO is normalised
magnetorquers are perfectly aligned with body frame axes
'''

def controlLaw (q_BO, v_Wb_m, v_Bb_m, dt):
	N=[1,1,1]                                 #[number of turns of magnetorquer aligned with x axis of body frame, " y axis ", " z axis "]
    A=[1,1,1]                                 #[area of magnetorquer aligned with x axis of body frame, " y axis ", " z axis "]
    Kp = np.array([[ -1,  0,  0], 
                   [  0, -1,  0], 
                   [  0,  0, -1]])
    Ki = np.array([[ -1,  0,  0], 
                   [  0, -1,  0], 
                   [  0,  0, -1]])
    Kd = np.array([[ -1,  0,  0], 
                   [  0, -1,  0], 
                   [  0,  0, -1]])
    v_e=np.array([])                          #error term in body frame (sin(theta)*UnitVectorOfAxisOfRotation)
    v_ie=np.array([0,0,0])                    #integral term
    Bmodsq = (v_Bb_m[0])**2 + (v_Bb_m[1])**2 + (v_Bb_m[2])**2 
    for i in range (0,3,1):
        e=np.append(e,[2*q[0]*q[i+1]])
        ie[i]=ie[i]+e[i]*dt
    v_m = (Kp.dot(v_e)+Ki.dot(v_ie)+Kd.dot(v_Wb_m))/Bmodsq
    v_mControl = np.cross(m,B)                #magnetic moment to be applied
    I=(v_mControl/A)/N                        #[current to be applied in magnetorquer aligned with x axis of body frame," y axis ", " z axis "]
    return I
#controlLaw([1,1,1,1],[0,0,0],[-1,0,1],1)

       