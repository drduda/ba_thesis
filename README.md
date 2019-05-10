# **Self calibrating eye tracking**
Usually eye-tracking devices need to be manually calibrated by the user. This one
calibrates itself without the user noticing at all. For a detailed description of 
the underlying concept have a look at 
[this paper](http://2013.petmei.org/wp-content/uploads/2013/09/petmei2013_session2_3.pdf).
I did this project for my bachelor thesis which is part of 
[eyeTrax](https://www.eyetrax.de/):
an eye tracking system for diagnosing light concussions based on occulomotoric deficits. 

#Installation
Create and activate the conda environment from the `environment.yml` file: <br>
`conda env create -f environment.yml` <br>
`conda activate ba_env` <br>
#Usage
Run `execute.py` to simulate and eye tracking session. For setting the parameters of the
simulation have a look at the documentation of `execution.py`.
###Using own data
Alternatively to simulating, you can use your own recorded tracking data. This is an
experimental feature yet. The recorded pupils need to be provided as 2D ellipse.
All pupils are saved in a python list and each pupil is a dictionary in the following
form. <br>
`{"x_center": self.ellipse.x_center,
                "y_center": self.ellipse.y_center,
                "maj": self.ellipse.major,
                "min": self.ellipse.minor,
"rot": self.ellipse.clockwise_rot}` <br>
The rotation is measured in degrees. You need to replace the `ellipse_param_list` with
your own in the `executin.py` file.