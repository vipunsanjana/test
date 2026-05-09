
### 1. Mathematical Explanation

**(a) Transforming the Problem**
The four extreme corners of a rectangle that is aligned with the coordinate axes define it completely. We may eliminate the interior and edge segments of the rectangles because the patrol path must be a convex polygon in order to attain the shortest length, and the edges of a convex polygon bridging discrete shapes will always rest on the extreme vertices of those shapes. Finding the shortest boundary that encloses the set of each machine's four corners simplifies the problem.

**(b) Validity of the Convex Hull**
The convex hull of a set of points in a two-dimensional plane is a universal definition of the shortest path encompassing that set. Imagine a rubber band that is stretched open to encircle every machine; it will snap tightly around the outermost edges when it is released. Drawing a straight line segment across a "dent" or concavity on any non-convex path can shorten it while still meeting the requirement of containing all interior points. Consequently, the boundary of the convex hull of every rectangle corner is the ideal patrol route.

**(c) Algorithmic Approach: Andrew's Monotone Chain**

We employ Andrew's Monotone Chain technique to quickly calculate the convex hull:

* Sorting: First, we arrange each corner point according to its X-coordinate (or, in the event of a tie, its Y-coordinate). This ensures that the points are processed linearly from left to right, enabling us to construct the hull in two separate halves with ease.

* Orientation Exams: The "upper" and "lower" parts of the hull are constructed by iterating through the sorted points. The orientation of the turn created by the new point and the final two points in our hull list is verified for each new point using the cross product. We eliminate the preceding point if the turn is collinear or clockwise since it produces a concavity and is not a part of the extreme boundary. When the remaining sequence forms a strictly counter-clockwise turn, we append the new point.

* Time Complexity: It takes $O(N)$ to extract $4N$ corners. The time complexity is dominated by sorting these $K = 4N$ points, which requires $O(K \log K)$, which reduces to $O(N \log N)$. The upper and lower hulls are constructed in $O(N)$ time by the consecutive linear scans. As a result, the total time complexity is $O(N \log N)$.

---

### 2. Mathematical Details (Formulas)

**Cross Product/Orientation Test** We compute the 2D cross product of vectors $\vec{OA}$ and $\vec{OB}$ to ascertain the orientation of an ordered triplet of points $O(x_0, y_0)$, $A(x_1, y_1)$, and $B(x_2, y_2)$.

$$ \text{Cross}(O, A, B) = (x_1 - x_0)(y_2 - y_0) - (y_1 - y_0)(x_2 - x_0) $$

* The points make an anticlockwise turn if $\text{Cross}(O, A, B) > 0$.
* The points make a clockwise turn if $\text{Cross}(O, A, B) < 0$.
* The points are collinear if $\text{Cross}(O, A, B) = 0$.

The Euclidean Distance
The Pythagorean theorem provides the straight-line distance $d$ between two points $P_1(x_1, y_1)$ and $P_2(x_2, y_2)$:

d(P_1, P_2) = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2} $$

The Convex Hull's Perimeter
The total patrol path length $P$ is the sum of the distances between neighboring vertices, looping back to the beginning, given the final ordered set of $m$ vertices that form the convex hull $H = {\H_0, H_1, \dots, H_{m-1}\}$.
$$ P = \sum_{i=0}^{m-1} d(H_i, H_{(i+1) \bmod m}) $$


---

### 3. Code Solution

The following Python implementation satisfies all constraints and achieves.

```python
import sys
import math

def cross_product(o, a, b):
    """
    Returns the 2D cross product of vectors OA and OB.
    Positive if O, A, B form a counter-clockwise turn.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def distance(p1, p2):
    """Calculates the Euclidean distance between two points."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def compute_convex_hull(points):
    """
    Computes the convex hull of a set of 2D points using Andrew's Monotone Chain.
    Returns a list of vertices forming the hull in counter-clockwise order.
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
    # Read all lines from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
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
    print(f"{perimeter:.6f}")

if __name__ == '__main__':
    solve()

```
