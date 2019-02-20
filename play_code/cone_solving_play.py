import sympy as sy
import numpy as np
import math
import matplotlib.pyplot as plt

'''
Assume simplest case. 
Take 9 Ellipses points + vertex
'''
#CONSTANTS
#Number of points
point_amount = 9
ellipse_center = (0,2)
y_depth = 1
#TODO https://docs.sympy.org/latest/modules/geometry/ellipses.html
#TODO ellipse is an own class in sympy
teta = np.arange(0,2*math.pi, 2*math.pi/(point_amount-1))

ellipse_x = ellipse_center[0] + 2*np.cos(teta)
ellipse_z = ellipse_center[1] + 0.5*np.sin(teta)

#%%
plt.plot(ellipse_x, ellipse_z)
plt.axis('equal')
plt.show()

#%%
x,y = sy.symbols('x y')
f = sy.Eq(5*x + 3 + y,0)
f2 = f.subs(x,1)

#Funktioniert, keine in_place manipulation





a,b,c,d,e,f,g,h,i, x, y, z = sy.symbols('a b c d e f g h i x y z')
implicit_equations = a*x**2 + b*x*y + c*x*z + d*y**2 + e*y*z + f*z**2 + g*x + h*y + z + i


#Homogenous Linear solvable system
eqns = []
for idx in range(point_amount):
    #Cone vertex is appended
    if idx == point_amount-1:
        substituted = implicit_equations.subs([(x,0),(y,0),(z,0)])
    elif idx < 3:
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

implicit_equations.subs(subs_list)