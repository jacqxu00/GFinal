from display import *
from matrix import *
from math import *

def add_box( points, x, y, z, width, height, depth ):
    add_edge(points, x, y, z, x+width, y, z)
    add_edge(points, x, y, z, x, y-height, z)
    add_edge(points, x, y, z, x, y, z-depth)
    add_edge(points, x+width, y, z, x+width, y-height, z)
    add_edge(points, x, y-height, z, x+width, y-height, z)
    add_edge(points, x+width, y, z, x+width, y, z-depth)
    add_edge(points, x, y-height, z, x, y-height, z-depth)
    add_edge(points, x+width, y-height, z, x+width, y-height, z-depth)
    add_edge(points, x, y, z-depth, x+width, y, z-depth)
    add_edge(points, x, y, z-depth, x, y-height, z-depth)
    add_edge(points, x+width, y, z-depth, x+width, y-height, z-depth)
    add_edge(points, x, y-height, z-depth, x+width, y-height, z-depth)

def add_sphere( points, cx, cy, cz, r, step ):
    for edge in generate_sphere(points, cx, cy, cz, r, step):
        add_edge(points, edge[0], edge[1], edge[2],
                     edge[0] + 1, edge[1] + 1, edge[2] + 1)
        
def generate_sphere( points, cx, cy, cz, r, step ):
    i0 = 1
    ans = []
    ans.append([r + cx, cy, cz])
    while i0 <= step:
        t0 = float(i0)/step
        i = 1
        while i <= step/2:
            t = float(i)/step
            x = r * math.cos(2 * math.pi * t) + cx
            y = r * math.sin(2 * math.pi * t) * math.cos(2 * math.pi * t0) + cy
            z = r * math.sin(2 * math.pi * t) * math.sin(2 * math.pi * t0) + cz
            edge = [x,y,z]
            ans.append(edge)
            i+=1
        i0+=1
    return ans

def add_torus( points, cx, cy, cz, r0, r1, step ):
    for edge in generate_torus(points, cx, cy, cz, r0, r1, step):
        add_edge(points, edge[0], edge[1], edge[2],
                     edge[0] + 1, edge[1] + 1, edge[2] + 1)

def generate_torus( points, cx, cy, cz, r0, r1, step ):
    i0 = 1
    ans = []
    ans.append([r0 + r1 + cx, cy, r1 + cz])
    while i0 <= step:
        t0 = float(i0)/step
        i = 1
        while i <= step:
            t = float(i)/step
            x = math.cos(2 * math.pi * t0) * (r0 * math.cos(2 * math.pi * t) + r1) + cx
            y = r0 * math.sin(2 * math.pi * t) + cy
            z = -1 * math.sin(2 * math.pi * t0) * (r0 * math.cos(2 * math.pi * t) + r1) + cz
            edge = [x,y,z]
            ans.append(edge)
            i+=1
        i0+=1
    return ans

def add_cylinder( points, cx, cy, cz, r, h, step ):
    points = generate_cylinder(cx, cy, cz, r, h, step)
    print points
    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( edges, points[p0][0],
                                 points[p0][1],
                                 points[p0][2],
                                 points[p1][0],
                                 points[p1][1],
                                 points[p1][2],
                                 points[p2][0],
                                 points[p2][1],
                                 points[p2][2])
            if longt != 0:
                add_polygon( edges, points[p0][0],
                        points[p0][1],
                                 points[p0][2],
                                 points[p2][0],
                                 points[p2][1],
                                 points[p2][2],
                                 points[p3][0],
                                 points[p3][1],
                                 points[p3][2])

def generate_cylinder( points, cx, cy, cz, r, h, step ):
    points = []
    move_start = 0
    move_stop = step
    circ_start = 0
    circ_stop = step
    
    for movement in range(move_start, move_stop):
        move = movement/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)
            
            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) + move * h + cy
            z = r * math.sin(math.pi * circ) + cz
            
            points.append([x,y,z])
    return points
        
def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1

def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
