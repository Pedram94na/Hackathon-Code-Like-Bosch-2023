"""

    """

from pathlib import Path

import numpy as np
import pandas as pd
from shapely.geometry import LineString , Point

class FPN :
    dta = 'DevelopmentData.xlsx'

class Cols :
    rx1 = 'FirstObjectDistance_X'
    ry1 = 'FirstObjectDistance_Y'
    rx2 = 'SecondObjectDistance_X'
    ry2 = 'SecondObjectDistance_Y'
    rx3 = 'ThirdObjectDistance_X'
    ry3 = 'ThirdObjectDistance_Y'
    rx4 = 'FourthObjectDistance_X'
    ry4 = 'FourthObjectDistance_Y'

    v = 'VehicleSpeed'

    rvx1 = 'FirstObjectSpeed_X'
    rvy1 = 'FirstObjectSpeed_Y'
    rvx2 = 'SecondObjectSpeed_X'
    rvy2 = 'SecondObjectSpeed_Y'
    rvx3 = 'ThirdObjectSpeed_X'
    rvy3 = 'ThirdObjectSpeed_Y'
    rvx4 = 'FourthObjectSpeed_X'
    rvy4 = 'FourthObjectSpeed_Y'

    yr = 'YawRate'
    t = 'Timestamp'

    dt = 'Delta_T'
    da = 'Delta_Angle'
    a = 'Angle'
    vx = 'VehicleSpeed_X'
    vy = 'VehicleSpeed_Y'
    dx = 'Delta_X'
    dy = 'Delta_Y'
    x = 'Vehicle_X'
    y = 'Vehicle_Y'

    x1 = 'Object1_X'
    y1 = 'Object1_Y'
    x2 = 'Object2_X'
    y2 = 'Object2_Y'
    x3 = 'Object3_X'
    y3 = 'Object3_Y'
    x4 = 'Object4_X'
    y4 = 'Object4_Y'

    vx1 = 'Object1Speed_X'
    vy1 = 'Object1Speed_Y'
    vx2 = 'Object2Speed_X'
    vy2 = 'Object2Speed_Y'
    vx3 = 'Object3Speed_X'
    vy3 = 'Object3Speed_Y'
    vx4 = 'Object4Speed_X'
    vy4 = 'Object4Speed_Y'

    v1 = 'Object1Speed'
    v2 = 'Object2Speed'
    v3 = 'Object3Speed'
    v4 = 'Object4Speed'

    i1x = 'Object1Intersection_X'
    i1y = 'Object1Intersection_Y'
    i2x = 'Object2Intersection_X'
    i2y = 'Object2Intersection_Y'
    i3x = 'Object3Intersection_X'
    i3y = 'Object3Intersection_Y'
    i4x = 'Object4Intersection_X'
    i4y = 'Object4Intersection_Y'

fpn = FPN()
c = Cols()

def find_intersection_point(px , py , vx , vy , p1x , p1y , v1x , v1y) :
    if np.isnan(px) :
        return np.nan , np.nan

    if px == p1x and py == p1y :
        return px , py

    elif vx == 0 and v1x == 0 and vy == 0 and v1y == 0 :
        return np.nan , np.nan

    elif (vx == 0 and vy == 0) and (v1x != 0 or v1y != 0) :
        a = Point(px , py)
        b = Point(p1x , p1y)
        c = Point(p1x + v1x , p1y + v1y)

        line = LineString([b , c])
        dist = line.distance(a)
        if dist < 1 :
            return px , py
        else :
            return np.nan , np.nan

    elif (v1x == 0 and v1y == 0) and (vx != 0 or vy != 0) :
        a = Point(px , py)
        b = Point(p1x , p1y)
        c = Point(px + vx , py + vy)

        line = LineString([b , c])
        dist = line.distance(a)
        if dist < 1 :
            return p1x , p1y
        else :
            return np.nan , np.nan

    else :
        a = Point(px , py)
        b = Point(px + vx , py + vy)
        c = Point(p1x , p1y)
        d = Point(p1x + v1x , p1y + v1y)

        if (b.y - a.y) / (b.x - a.x) == (d.y - c.y) / (d.x - c.x) :
            return np.nan , np.nan

        else :
            line1 = LineString([a , b])
            line2 = LineString([c , d])

            int_pt = line1.intersection(line2)

            try :
                return int_pt.x , int_pt.y
            except :
                return np.nan , np.nan

vect_find_int_point = np.vectorize(find_intersection_point)

def main() :
    pass

    ##
    df = pd.read_excel(fpn.dta , index_col = 0)

    ##
    # assert time is monotonic increasing and unique across dataset
    assert df[c.t].is_monotonic_increasing
    assert df[c.t].is_unique

    ##
    # calculate delta time
    df[c.dt] = df[c.t].diff()

    ##
    # calculate delta angle
    df[c.da] = df[c.yr] * df[c.dt]

    ##
    # calculate angle
    df[c.a] = df[c.da].cumsum()

    ##
    # calculate vehicle speed x and y
    df[c.vx] = df[c.v] * np.cos(df[c.a])
    df[c.vy] = df[c.v] * np.sin(df[c.a])

    ##
    # calculate delta x and y
    df[c.dx] = df[c.vx] * df[c.dt]
    df[c.dy] = df[c.vy] * df[c.dt]

    ##
    # calculate x and y
    df[c.x] = df[c.dx].cumsum()
    df[c.y] = df[c.dy].cumsum()

    ##
    # calculate objects x positions (absolute)
    duo = {
            c.x1 : c.rx1 ,
            c.x2 : c.rx2 ,
            c.x3 : c.rx3 ,
            c.x4 : c.rx4 ,
            }

    for ax , rx in zip(duo.keys() , duo.values()) :
        df[ax] = df[c.x] + df[rx]

    ##
    # calculate objects y positions (absolute)
    duo = {
            c.y1 : c.ry1 ,
            c.y2 : c.ry2 ,
            c.y3 : c.ry3 ,
            c.y4 : c.ry4 ,
            }

    for ay , ry in zip(duo.keys() , duo.values()) :
        df[ay] = df[c.y] + df[ry]

    ##
    # calculate objects x speeds (absolute)
    duo = {
            c.vx1 : c.rvx1 ,
            c.vx2 : c.rvx2 ,
            c.vx3 : c.rvx3 ,
            c.vx4 : c.rvx4 ,
            }

    for avx , rvx in zip(duo.keys() , duo.values()) :
        df[avx] = df[rvx] + df[c.vx]

    ##
    # calculate objects y speeds (absolute)
    duo = {
            c.vy1 : c.rvy1 ,
            c.vy2 : c.rvy2 ,
            c.vy3 : c.rvy3 ,
            c.vy4 : c.rvy4 ,
            }

    for avy , rvy in zip(duo.keys() , duo.values()) :
        df[avy] = df[rvy] + df[c.vy]

    ##
    # calculate objects speeds
    duo = {
            c.v1 : (c.vx1 , c.vy1) ,
            c.v2 : (c.vx2 , c.vy2) ,
            c.v3 : (c.vx3 , c.vy3) ,
            c.v4 : (c.vx4 , c.vy4) ,
            }

    for v , (vx , vy) in zip(duo.keys() , duo.values()) :
        df[v] = np.sqrt(df[vx] ** 2 + df[vy] ** 2)

    ##
    # calculate intersection points

    duo = {
            (c.i1x , c.i1y) : (c.x1 , c.y1 , c.vx1 , c.vy1) ,
            (c.i2x , c.i2y) : (c.x2 , c.y2 , c.vx2 , c.vy2) ,
            (c.i3x , c.i3y) : (c.x3 , c.y3 , c.vx3 , c.vy3) ,
            (c.i4x , c.i4y) : (c.x4 , c.y4 , c.vx4 , c.vy4) ,
            }

    fu = find_intersection_point

    for (ix , iy) , (x , y , vx , vy) in zip(duo.keys() , duo.values()) :
        df[[ix , iy]] = df.apply(lambda s : fu(s[c.x] ,
                                               s[c.y] ,
                                               s[c.vx] ,
                                               s[c.vy] ,
                                               s[x] ,
                                               s[y] ,
                                               s[vx] ,
                                               s[vy]) ,
                                 axis = 1 ,
                                 result_type = 'expand')

##

##


if __name__ == "__main__" :
    main()
    print(f'{Path(__file__).name} Done!')

##


def test() :
    pass

    ##
    import shapely
    from shapely.geometry import LineString , Point

    A = Point(0 , 0)
    B = Point(1 , 1)
    C = Point(1 , 0)
    D = Point(0 , 1)

    line1 = LineString([A , B])
    line2 = LineString([C , D])

    int_pt = line1.intersection(line2)
    point_of_intersection = int_pt.x , int_pt.y
    print(point_of_intersection)

    ##
    find_intersection_point(0 , 0 , 1 , 1 , 1 , 0 , -1 , 1)

    ##

    ##
