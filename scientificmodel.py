import numpy as np 
import math as math
import qnv as qnv
import frames as fs
import constants_1U as constants
from satellite import Satellite

def sm_J2_mag(sat): 
	v_mag_i=sat.getMag_i()
	J2data=sat.getJ2Data()
	v_pos_m=np.array([J2data[0],J2data[1],J2data[2]])
	v_vel_m=np.array([J2data[3],J2data[4],J2data[5]])
	v_mag_o=ecif2orbit(v_pos_m,v_vel_m,v_mag_i)
	return v_mag_o

def sm_gps_mag(sat): 
	v_mag_i=sat.getMag_i()
	gpsdata=sat.getgpsData()
	v_pos_m=np.array([gpsdata[0],gpsdata[1],gpsdata[2]])
	v_vel_m=np.array([gpsdata[3],gpsdata[4],gpsdata[5]])
	v_mag_o=ecif2orbit(v_pos_m,v_vel_m,v_mag_i)
	return v_mag_o

def sm_J2_sun(sat): 
	v_sun_i=sat.getSun_i()
	J2data=sat.getJ2Data()
	v_pos_m=np.array([J2data[0],J2data[1],J2data[2]])
	v_vel_m=np.array([J2data[3],J2data[4],J2data[5]])
	v_sun_o=ecif2orbit(v_pos_m,v_vel_m,v_sun_i)
	return v_sun_o

def sm_gps_b(sat): 
	v_sun_i=sat.getSun_i()
	gpsdata=sat.getgpsData()
	v_pos_m=np.array([gpsdata[0],gpsdata[1],gpsdata[2]])
	v_vel_m=np.array([gpsdata[3],gpsdata[4],gpsdata[5]])
	v_sun_o=ecif2orbit(v_pos_m,v_vel_m,v_sun_i)
	return v_sun_o
