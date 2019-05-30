import execute as exe
import numpy as np
import matplotlib.pyplot as plt

def run(*argv, eye_center=[0, -5, 0], visualize=True):
    """
    Can take noising functions to manipulate the input data
    :return:
    """
    sess = exe.Session(eye_center=eye_center)
    input_data = sess.simulate_input_data()
    if argv:
        for noising_function in argv:
            input_data = noising_function(input_data, sess)
    return sess.reprojection(input_data, visualize=visualize)


"""
Now the performance will be analyzed for different eye center positions.
Therefore, the eye will be initialzed in a grid (for the x, y axis from -2 to 2) 
"""
def run_with_grid_eye_center(min=-2, max=2, steps=11):
    x = np.linspace(min, max, steps)
    y = np.linspace(min, max, steps)
    X, Y = np.meshgrid(x, y)
    distance_grid = np.empty(shape=(steps, steps))
    for i in range(steps):
        for j in range(steps):
            _, distance_grid[i, j] = run(eye_center=[x[i], -5, y[j]], visualize=False)
    plt.contourf(X, Y, distance_grid, 20, cmap='RdGy')
    plt.colorbar()

    plt.show()
    return distance_grid


run_with_grid_eye_center()
#%%
# Shifted eye center is tried out
run(eye_center=[1.0, -5.0, 1.0])

#%%%
# Four different eye centers are tried out for error detection
run(eye_center=[1.0, -5.0, 1.0])
run(eye_center=[-1.0, -5.0, 1.0])
run(eye_center=[1.0, -5.0, -1.0])
run(eye_center=[-1.0, -5.0, -1.0])

#%%
# Now all pupils under the projected eye center will be removed
# Will this increase the performance?
def remove_bottom_pupils(input_data, sess):
    eye_center_y = sess.projected_eye_center[1]
    input_data = [el for el in input_data if el['y_center']>eye_center_y]
    return input_data
run(remove_bottom_pupils, eye_center=[1.0, -5.0, 1.0])

#%%
