from execute import simulate_input_data, reprojection
import execute
import numpy as np


def run(noising_function=None):
    """
    Takes a function that noisy the input data.
    :return:
    """
    input = simulate_input_data()
    if noising_function:
        input = noising_function(input)
    reprojection(input)

#%%
#First result for shifted eye center
execute.EYE_CENTER = np.array([1.0, -5.0, 1.0])
run()

#%%%
# Different eye centers are tried out for error detectin
execute.EYE_CENTER = np.array([1.0, -5.0, 1.0])
run()
execute.EYE_CENTER = np.array([-1.0, -5.0, 1.0])
run()
execute.EYE_CENTER = np.array([1.0, -5.0, -1.0])
run()
execute.EYE_CENTER = np.array([-1.0, -5.0, -1.0])
run()

