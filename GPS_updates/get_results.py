#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       animals.py
#
#       Copyright 2012 Oleguer Sagarra <oleguer.sagarra@gmail.com>
#       and Mario Gutiérrez-Roig <mariogutierrezroig@ub.edu>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#       Contains:
#             General functions
#             
#

### Global Variables ###

zone=31 # zone utm 31T
origin=(431769,4582211) # map origin #Coordenades geodèsiqueS: N41º23.312 E02º11.034

### Modules ###

import numpy as np
from math import pow, sqrt

try:
    import pyproj as pr
except ImportError:
    print "Please install pyproj module"
utm = pr.Proj(ellips="WGS84", proj="utm", zone=zone, preserve_units=False) # Define ellipsoid and UMT zone

### Functions ###

def results (distance, time, npoles):
    """ Provides the results in comparison with the animals.
     
        Input:  - Velocity
                - Time
                - Number of found poles
        
        Output: - Dictionary with animals sorted by time
                - Some sample points
    """

    if time == 0 or npoles == 0:
        A = {'user': time, 'animal': 0, 'polen': 0}
    else:
        vel = distance / time
        A = {'user': time, 'animal': time_animal(vel, npoles), 'polen': time_polen(vel, npoles)}

    return A

def time_animal (vel, npoles):
    """ Calculates the time needed for a "animal movement" to find the
        poles. Coeficcients A, B, C and D come from numerical
        simulations.
    
        Input:  - Velocity
                - Number of found poles
        
        Output: - Dictionary with animals sorted by time
                - Some sample points
    """
    A = 1.32
    B = -0.47
    C = 38235
    D = 0.52
    
    beta = A * pow (vel, B)
    tanimal = (C * pow(beta, D) ) * (npoles / 10.)
    
    return tanimal

def time_polen (vel, npoles):
    """ Calculates the time needed for a "polen movement" to find the
        poles. Coeficcients A, B, C and D come from numerical
        simulations.
    
        Input:  - Velocity
                - Number of found poles
        
        Output: - Dictionary with animals sorted by time
                - Some sample points
    """
    A = 1.41
    B = -0.5
    C = 859887
    D = 0.99
    
    beta = A * pow (vel, B)
    tpolen = (C * pow(beta, D) ) * (npoles / 10.)
    
    return tpolen

def lonlat_2_UTM(points,origin,zone,time=False):
    """ Converts lon-lat-time input to x-y-files on given UTM zone with given origin
    input:
        - origin must be a 2 index tupple (x,y)
        - np.array with at least 2 columns lat-lon
        - Scalar UTM zone
    output:
        - array with lat,lon
    """
    points = np.array(points)
    rot = np.array(utm(points.T[0],points.T[1])).T-origin # transformacio geo (lon-lat)
    
    xy = []
    for a in rot: 
        xy.append([a[0]*np.cos(np.pi/4)-a[1]*np.sin(np.pi/4), a[0]*np.sin(np.pi/4)+a[1]*np.cos(np.pi/4)])

    if time:
        return np.array([xy.T[0],xy.T[1],points.T[-1]]).T # transformacio geo (lon-lat)
    else:
        return np.array(xy) # transformacio geo (lon-lat)

#### Cheat sheet #####

def calc_distance(update_list):
    """ Aprofita per calcular le sposicions directament en UTM """
    utm = lonlat_2_UTM(update_list,origin,zone)
    diff = np.diff(utm,axis=0)
    d = 0
    for x,y in B: d=d+np.sqrt(x*x+y*y)
    return d
