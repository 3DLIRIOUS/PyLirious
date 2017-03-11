from setuptools import setup

setup(name='pylirious',
      version='20170311',
      description='3D model creation and processing with Python',
      url='https://github.com/3DLIRIOUS/pylirious',
      author='3DLirious',
      author_email='3DLirious@gmail.com',
      license='LGPL-2.1',
      packages=['pylirious'],
      install_requires=['meshlabxml',],
      include_package_data=True)
