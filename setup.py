from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup
 
d = generate_distutils_setup(
    packages=['rknn_yolo'],
    package_dir={'': 'src'}
)
 
setup(**d)