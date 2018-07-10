import numpy as np
import math
import qnv as qnv
import frames as f
import constants_1U as constants
import satellite as sat 
import power as pow

sgp_output = np.genfromtxt('sgp_output.csv', delimiter=",")
si_output = np.genfromtxt('si_output.csv', delimiter=",")
light_output = np.genfromtxt('light_output.csv', delimiter=",")
T = si_output[:,0] #storing first element as time

N = len(T)
power_output = np.zeros((N,7))

state=np.array([1,0,0,0,0,0,0])

#Make satellite object
advitiy = sat.Satellite(state,0)

for i in range(N):
    #setting time
    advitiy.setTime(T[i])
    #dt = T[i+1] - T[i]
    
    #getting light, sun vector, position, velocity from csv files
    light = light_output[i,1]
    v_sun_i = si_output[i,1:4].copy()  
    v_pos_i = sgp_output[i,1:4].copy()
    v_vel_i = sgp_output[i,4:7].copy()
    
    #calculating sun vector body and orbit frame
    v_sun_o = f.ecif2orbit(v_pos_i,v_vel_i,v_sun_i)
    v_sun_b = v_sun_o.copy()
    
    #setting attributes to satellite
    advitiy.setPos(v_pos_i)
    advitiy.setVel(v_vel_i)
    advitiy.setSun_i(v_sun_i)
    #advitiy.setSun_o(v_sun_o)
    advitiy.setSun_b_m(v_sun_b)
    advitiy.setLight(light)
    
    power_arr = pow.power(advitiy)
    
    power_output[i,0] = T[i]
    power_output[i,1:7] = power_arr.copy();
    
np.savetxt("power_output.csv", power_output, delimiter=',')