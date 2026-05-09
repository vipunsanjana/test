import sys
import math
import logging

# or change to INFO/WARNING to reduce noise.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def cross_product(o, a, b):
    """
    Args:        o, a, b: Tuples representing the (x, y) coordinates of three points.
    Returns:      The cross product of the vectors OA and OB, where O is the origin
                    point, A and B are the other two points. The cross product is positive if OAB makes a left turn, negative for a right turn, and zero if the points are collinear.
    Description:  Computes the cross product of the vectors OA and OB using the formula: (Ax - Ox) * (By - Oy) - (Ay - Oy) * (Bx - Ox). This is a common operation in computational geometry to determine the relative orientation of three points.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def distance(p1, p2):
    """
    Args:        p1, p2: Tuples representing the (x, y) coordinates of two points.
    Returns:      The Euclidean distance between the two points.
    Description:  Computes the Euclidean distance between two points using the formula: distance = sqrt((x2 - x1)^2 + (y2 - y1)^2). This is implemented using math.hypot for numerical stability and readability.
    """
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def compute_convex_hull(points):
    """
    Args:        points: A list of tuples representing the (x, y) coordinates of points.
    Returns:      A list of tuples representing the vertices of the convex hull in counter-clockwise order.
    Description:  Computes the convex hull of a set of points using the Monotone Chain algorithm, which has a time complexity of O(n log n). The algorithm first sorts the points and then constructs the lower and upper hulls. Finally, it concatenates the two hulls to form the complete convex hull.
    """
    # Remove duplicates and sort primarily by x, then by y
    points = sorted(list(set(points)))
    
    if len(points) <= 1:
        return points

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper hull 
    # (excluding the last point of each half because it is repeated)
    return lower[:-1] + upper[:-1]

def solve():

    with open("input.txt", "r") as f:
        input_data = f.read().split()
    
    if not input_data:
        logger.error("No input data found.")
        return
        
    N = int(input_data[0])
    
    # Extract the 4 corners for each of the N rectangles
    points = []
    idx = 1
    for _ in range(N):
        x1 = float(input_data[idx])
        y1 = float(input_data[idx+1])
        x2 = float(input_data[idx+2])
        y2 = float(input_data[idx+3])
        idx += 4
        
        # Append all four corners
        points.append((x1, y1))
        points.append((x1, y2))
        points.append((x2, y1))
        points.append((x2, y2))

    # Compute the optimal patrol path vertices
    hull = compute_convex_hull(points)

    # Compute total perimeter
    perimeter = 0.0
    m = len(hull)
    if m > 1:
        for i in range(m):
            perimeter += distance(hull[i], hull[(i + 1) % m])
            
    # Output the result with required precision
    logger.debug(f"Convex Hull Points: {hull}")
    logger.debug(f"Perimeter: {perimeter}")
    logger.info(f"{perimeter:.6f}")

if __name__ == '__main__':
    solve()
