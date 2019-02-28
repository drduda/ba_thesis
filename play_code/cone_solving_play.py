import sympy as sy
import numpy as np
import math
import matplotlib.pyplot as plt
from plot_implicit import plot_implicit
import projection

#%%
'''
Assume simplest case. 
Take 9 Ellipses points + vertex
'''
#CONSTANTS
#Number of points
point_amount = 6
#TODO https://docs.sympy.org/latest/modules/geometry/ellipses.html
#TODO ellipse is an own class in sympy

e = projection.Eye()
p = projection.Pupil(e, [0,0,0.2])
y_depth = e.display_distance
ellipse = p.ellipse.points_on_ellipse_T
print("Ellispe minor: " + str(p.ellipse.minor/2))
print("Ellipse major: " + str(p.ellipse.major/2))

ellipse_x = [ellipse[i][0] for i in range(0,100,20)]
ellipse_z = [ellipse[i][1] for i in range(0,100,20)]

plt.plot(ellipse_x, ellipse_z)
plt.axis('equal')
plt.xlabel('x')
plt.ylabel('z')
plt.show()

#%%

a,b,c,d,e,f,g,h,i, x, y, z = sy.symbols('a b c d e f g h i x y z')
implicit_equations = a*x**2 + b*x*y + c*x*z + d*y**2 + e*y*z + f*z**2 + g*x + h*y + z + i

implicit_equations = a*x**2 + b*x*y + c*x*z + d*y**2 + e*y*z + z**2

#Homogenous Linear solvable system
eqns = []
for idx in range(point_amount):
    #Cone vertex is appended
    if idx == point_amount-1:
        substituted = implicit_equations.subs([(x,0),(y,0),(z,0)])
    #TODO CHANGE BACK
    elif idx < 10:
        # The first three points are mirrored at vertex point (0,0,0) meaning times (-1) at each point
        substituted = implicit_equations.subs([(x,-ellipse_x[idx]), (y, -y_depth), (z,-ellipse_z[idx])])
    else:
        substituted = implicit_equations.subs([(x,ellipse_x[idx]), (y, y_depth), (z,ellipse_z[idx])])
    eqns.append(substituted)

coefficients = sy.linsolve(eqns, a, b, c, d, e, f, g, h, i)

#TODO ÜBERPRÜFE OB ARGS[1] EXESTIERT
subs_list = []
#coeff list muss eventuell erweitert werden
symbol_list = [a, b, c, d, e, f, g, h, i]
for idx in range(len(coefficients.args[0])):
    subs_list.append((symbol_list[idx], coefficients.args[0][idx]))

result = implicit_equations.subs(subs_list)
print(result)

#%%
#Plane
plane_normal = np.array([0,1,0])
shifted_y_height = -10

#Make roation matrix
for rotation in range(-90,91,10):
    if rotation != 0:
        alpha = math.radians(rotation)
        rotate_matrix = np.array([[1, 0, 0],
                                  [0, math.cos(alpha), -math.sin(alpha)],
                                  [0, math.sin(alpha), math.cos(alpha)]])
        rotated_normal = np.dot(rotate_matrix, plane_normal)
        # Make Plane n(x-a)=0
        z_value = -rotated_normal[1]/rotated_normal[2]*(y-shifted_y_height)

        print(rotation)
        #Put in z_value
        intersection = sy.simplify(result.subs(z, z_value))
        print(intersection)
