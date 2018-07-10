import numpy as np
import math
import qnv as qnv
import frames as fs
import constants_1U as constants
from satellite import Satellite

'''
this function takes input:
    satellite class
    (sun vector in body frame)
             gives output:
    power received by solar panels

'''    
        
def power(sat):
    v_S1  = constants.v_Ax                                   #area in metre square
    v_S2  = (-1)*constants.v_Ax
    v_S3  = constants.v_Ay
    v_S4  = (-1)*constants.v_Ay
    v_S5  = constants.v_Az
    v_S6  = (-1)*constants.v_Az
    area_vector = np.array([v_S1,v_S2,v_S3,v_S4,v_S5,v_S6])
    area = np.array([v_S1,(-1)*v_S2,v_S3,(-1)*v_S4,v_S5,(-1)*v_S6])
    v_S1_norm = np.linalg.norm(v_S1) 
    face_vector = area_vector/(v_S1_norm)
    EFFICIENCY = 0.27
    INTENSITY = 1000                                         #in watts per metre square
    MIN_ANGLE = 60
    MIN_VAL = math.cos(math.radians(MIN_ANGLE))
    v_sun_b_m = sat.getSun_b_m()
    #v_sun_b_m = np.array([1,1,1])
    cos_values = np.array([])
    for i in range (0,6):
            cos_values = np.append(cos_values,[np.dot(face_vector[i],v_sun_b_m)])
    LIGHT=sat.getLight()
    for i in range (0,6):
        if (cos_values[i]<MIN_VAL):
            cos_values[i]=0
    effective_area=np.array([])
    for i in range (0,6):
        effective_area=np.append(effective_area,[(area[i])*cos_values[i]])    #area of each side is 0.01 msq
    POWER= np.array([])
    for i in range (0,6):
        POWER = np.append(EFFICIENCY*INTENSITY*effective_area[i])
    if (LIGHT==0 or LIGHT==0.5):
        POWER=[0,0,0,0,0,0]
    return POWER









