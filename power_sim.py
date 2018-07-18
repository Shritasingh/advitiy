import matplotlib.pyplot as plt
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
energy=0
N = len(T)
power_output = np.zeros((N,9))
energy_output = np.zeros((36,7))

state=np.array([1,0,0,0,0,0,0])

#Make satellite object
advitiy = sat.Satellite(state,0)

for j in range(0,360,10):

    x=0
    y=0
    z=0

    Rx=np.array([[1.0,0.0,0.0],[0.0,math.cos(x),math.sin(x)],[0.0,math.sin(-x),math.cos(x)]])
    Ry=np.array([[math.cos(y),0.0,math.sin(-y)],[0.0,1.0,0.0],[math.sin(y),0.0,math.cos(y)]])
    Rz=np.array([[math.cos(z),math.sin(-z),0.0],[math.sin(z),math.cos(z),0.0],[0.0,0.0,1.0]])
    R_orbit2body=Rx.dot(Ry).dot(Rz)

    for i in range(N):
        #setting time
        advitiy.setTime(T[i])
        dt = T[1] - T[0]
        #getting light, sun vector, position, velocity from csv files
        light = light_output[i,1]
        v_sun_i = si_output[i,1:4].copy()  
        v_pos_i = sgp_output[i,1:4].copy()
        v_vel_i = sgp_output[i,4:7].copy()
        
        #calculating sun vector body and orbit frame
        v_sun_o = f.ecif2orbit(v_pos_i,v_vel_i,v_sun_i)
        v_sun_b = R_orbit2body.dot(v_sun_o)
        
        #setting attributes to satellite
        advitiy.setPos(v_pos_i)
        advitiy.setVel(v_vel_i)
        advitiy.setSun_i(v_sun_i)
        #advitiy.setSun_o(v_sun_o)
        advitiy.setSun_b_m(v_sun_b)
        advitiy.setLight(light)
        
        power_arr = pow.power(advitiy)
        #energy=energy+power_arr[6]*dt
        energy_output[j,0] = j
        energy_output[j,1] = energy_output[j,1]+power_arr[0]*dt #for each side:x,-x,y,-y,z,-z
        energy_output[j,2] = energy_output[j,2]+power_arr[1]*dt #for each side:x,-x,y,-y,z,-z
        energy_output[j,3] = energy_output[j,3]+power_arr[2]*dt #for each side:x,-x,y,-y,z,-z
        energy_output[j,4] = energy_output[j,4]+power_arr[3]*dt #for each side:x,-x,y,-y,z,-z
        energy_output[j,5] = energy_output[j,5]+power_arr[4]*dt #for each side:x,-x,y,-y,z,-z
        energy_output[j,6] = energy_output[j,6]+power_arr[5]*dt #for each side:x,-x,y,-y,z,-z

        
        #power_output[i,7] = power_arr[6] #total power at t=T[i]
#power_output[0,8]=energy    
np.savetxt("energy_output.csv", energy_output, delimiter=',')
plt.plot(energy_output[:,0],energy_output[:,1],label='leading side')
plt.plot(energy_output[:,0],energy_output[:,2],label='lagging side')
plt.plot(energy_output[:,0],energy_output[:,3],label='anti-sun side')
plt.plot(energy_output[:,0],energy_output[:,4],label='sun side')
plt.plot(energy_output[:,0],energy_output[:,5],label='nadir')
plt.plot(energy_output[:,0],energy_output[:,6],label='zenith')
plt.legend(bbox_to_anchor=(1,1),bbox_transform=plt.gcf().transFigure)
plt.grid()
plt.show()
