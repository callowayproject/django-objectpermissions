from setuptools import setup
import objectpermissions, os

try:
    long_desc = open('README').read()
except IOError:
    long_desc = 'This is a way to add the ability to set and test permissions by model and assign permissions to individual users and groups'

try:
    version = objectpermissions.get_version()
except ImportError:
    version = ''

try:
    reqs = open(os.path.join(os.path.dirname(__file__),'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''

setup(name='django-objectpermissions',
      version=version,
      description='A method for adding object-level or row-level permissions',
      long_description=long_desc,
      author='Corey Oordt',
      author_email='coordt@washingtontimes.com',
      url='http://opensource.washingtontimes.com/projects/objectpermissions/',
      packages=['objectpermissions'],
      include_package_data=True,
      classifiers=[
          'Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Security',
          ],
      )