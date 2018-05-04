import numpy as np
import qnv as qnv
import frames as fs
from constants import *

'''
this funtion takes input:
    position of centre of mass of satellite in eci frame
    quarternion to convert vector in body frame to eci frame
    inertia matrix of satellite
             gives output:
    torque due to gravity gradient about centre of mass in body frame
''' 
def GG_torque (satellite) :
    q = satellite.getQ()                                   #body frame to eci frame??
    qi = qnv.quatInv(q)
    v_pos_sat_i = satellite.getPos()                       #pos vector in eci frame
    v_pos_sat_b = qnv.quatRotate(qi,v_pos_sat_i)           #pos vector in body frame
    pos_norm = np.linalg.norm(v_pos_sat_b)
    m_INERTIA = constants.m_INERTIA                        #how is this formed? can this be used directly?
    Mass_earth = constants.M
    G = constants.G
    v_T_gg_i = 3*Mass_earth*G*(np.linalg.cross(v_pos_sat_b,m_INERTIA.dot(v_pos_sat_b)))/(pos_norm**5)                                  
    return v_T_gg_b

'''
this function takes input:
    velocity of COM of satellite in eci frame
    quarternion to convert a vector in body frame to eci frame
    vector between COM and geometric centre expressed in body frame
              gives output:
    torque due to air drag about COM in body frame
'''
def Aero_torque(satellite):
    q = satellite.getQ()
    qi = qnv.quatInv(q)
    r_com_b = [1,1,1]                                                         # yet to include 
    density =  1                                                              # yet to include
    Cd = 1                                                                    # yet to include
    l = 0.1                            #length of cube in metres
    v_vel_i = satellite.getVel()                                              #velocity of COM in eci frame
    v_vel_b = qnv.quatRotate(qi,v_vel_i)                                      #velocity of COM in body frame
    vel_norm = np.linalg.norm(v_vel_b)
    area = l*l*(abs(np.dot([1.,0,0],v_vel_b))+abs(np.dot([0,1.,0],v_vel_b))+abs(np.dot([0,0,1.],v_vel_b)))
    v_T_ad_b = density*Cd/2*area*vel_norm*np.cross(r_com_b, v_vel_b)         
    return v_T_ad_b

'''
this function takes input:
    sun vector in eci frame
    quarternion to convert a vector in body frame to eci frame
    vector between COM and geometric centre expressed in body frame
              gives output:
    torque due to solar drag about COM in body frame
''' 
def Solar_torque(satellite):
    q=satellite.getQ()
    qi = qnv.quatInv(q)
    P = 1                                                                      # yet to include
    e = 1                                                                      # yet to include 
    r_com_b = [1,1,1]                                                          # yet to include
    l = 0.1  # metres, length of cube                                                      
    v_sv_i = satellite.getSun_i()                                             #sun vector in eci frame
    v_sv_b = qnv.quatRotate(qi,v_sv_i)                                        #sun vector in body frame  
    cosw1 = np.dot([1.,0.,0.] , v_sv_b)/np.linalg.norm(v_sv_b) 
    cosw2 = np.dot([0.,1.,0.] , v_sv_b)/np.linalg.norm(v_sv_b) 
    cosw3 = np.dot([0.,0.,1.] , v_sv_b)/np.linalg.norm(v_sv_b) 
    area  = (abs(cosw1) + abs(cosw2) + abs(cosw3))*l*l
    v_coswsq= np.array([abs(cosw1)*(cosw1),abs(cosw2)*(cosw2),abs(cosw3)*(cosw3)])
    v_T_sd_b = P*area*(1-e)/np.linalg.norm(v_sv_b)*np.cross(v_sv_b, r_com_b) + 2*e*P*l*l*np.cross (r_com_b , v_coswsq)
    return v_T_sd_b 

    
    
    

