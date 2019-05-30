import execute as exe
import numpy as np
import matplotlib.pyplot as plt

def run(*argv, eye_center=[0, -5, 0], noise_dev = None, visualize=True):
    """
    Can take noising functions as *argv to manipulate the input data
    :return:
    """
    sess = exe.Session(eye_center=eye_center)
    input_data = sess.simulate_input_data()
    if argv:
        for noising_function in argv:
            if noise_dev:
                input_data = noising_function(input_data, deviation=noise_dev)
            else:
                try:
                    input_data = noising_function(input_data)
                except TypeError:
                    input_data = noising_function(input_data, sess)
                else:
                    print("Noising function could not be called")
    return sess.reprojection(input_data, visualize=visualize)



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
"""
Now the performance will be analyzed for different eye center positions.
Therefore, the eye will be initialzed in a grid (for the x, y axis from -2 to 2) 
"""
def run_with_grid_eye_center(min=-2, max=2, steps=21, *argv):
    x = np.linspace(min, max, steps)
    y = np.linspace(min, max, steps)
    X, Y = np.meshgrid(x, y)
    distance_grid = np.empty(shape=(steps, steps))

    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            _, distance_grid[i, j] = run(*argv, eye_center=[xi, -5, yj], visualize=False)

    plt.contourf(X, Y, distance_grid, 20, cmap='Reds')
    plt.colorbar()
    plt.show()

    return distance_grid


run_with_grid_eye_center()

#%%
#Now the same noise is added to the maj and minor axis.
def add_scaling_noise(input_data):
    """
    Each ellipse is scaled randomly. Position and rotation stay the same.
    :param input_data:
    :return:
    """
    DEVIATION = 0.40
    for ellipse in input_data:
        noise = 1 + np.random.normal(DEVIATION)
        ellipse['maj'] *= noise
        ellipse['min'] *= noise
    return input_data


run(add_scaling_noise)

#%%
def add_noise_to_each_attribute(input_data, deviation):
    for ellipse in input_data:
        for attribute in ellipse:
            noise = 1 + np.random.normal(scale=deviation)
            ellipse[attribute] *= noise
    return input_data


run(add_noise_to_each_attribute, noise_dev=0.05)