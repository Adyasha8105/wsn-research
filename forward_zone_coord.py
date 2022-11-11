from shapely.geometry import LineString, Point, Polygon

def line_joining_centre(s, d):
    """
    Returns the line joining the centre of s to the centre of d.
    """
    m = (d[1] - s[1]) / (d[0] - s[0])
    b = s[1] - m * s[0]
    return m, b

def perpendicular_diameter(m, b, s, d): 
    """
    Returns the perpendicular diameter of the line with equation y = mx + b.
    """
    m = -1 / m
    bs = s[1] - m * s[0]
    bd = d[1] - m * d[0]
    return m, bs, bd

def point_of_intersection(r, s, d):
    """ 
    Returns the point of intersection of the line with equation y = mx + b.
    """
    # defining the source and destination circles 
    ps = Point(s[0], s[1]).buffer(r).boundary
    pd = Point(d[0], d[1]).buffer(r).boundary
    # defining the line
    center_joining_line = LineString([s, d])
    left_half = center_joining_line.parallel_offset(r, 'left')
    right_half = center_joining_line.parallel_offset(r, 'right')
    s_diameter = LineString([left_half.boundary.geoms[1], right_half.boundary.geoms[0]])
    d_diameter = LineString([left_half.boundary.geoms[0], right_half.boundary.geoms[1]])

    d1 = left_half.boundary.geoms[1]
    d2 = right_half.boundary.geoms[0]

    s1 = left_half.boundary.geoms[0]
    s2 = right_half.boundary.geoms[1]
    
    # print("Line passing through D")
    # print(left_half.boundary.geoms[1].x, left_half.boundary.geoms[1].y)
    # print(right_half.boundary.geoms[0].x, right_half.boundary.geoms[0].y)

    # print("Line passing through S")
    # print(left_half.boundary.geoms[0].x, left_half.boundary.geoms[0].y)
    # print(right_half.boundary.geoms[1].x, right_half.boundary.geoms[1].y)

    forward_zone = []
    forward_zone.append((s1.x, s1.y))
    forward_zone.append((s2.x, s2.y))
    forward_zone.append((d1.x, d1.y))
    forward_zone.append((d2.x, d2.y))

    return forward_zone

def inside_polygon(forward_zone, p): 
    """
    Returns true if the point is inside polygon
    """
    p = Point(p[0], p[1])
    polygon = Polygon(forward_zone)

    return p.within(polygon)
