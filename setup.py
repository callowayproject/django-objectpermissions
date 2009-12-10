from distutils.core import setup

try:
    long_desc = open('README').read()
except IOError:
    long_desc = 'This is a way to add the ability to set and test permissions by model and assign permissions to individual users and groups'

setup(name='objectpermissions',
      version='0.1a',
      description='A method for adding object-level or row-level permissions',
      long_description=long_desc,
      author='Corey Oordt',
      author_email='coordt@washingtontimes.com',
      url='http://opensource.washingtontimes.com/projects/objectpermissions/',
      packages=['objectpermissions'],
      classifiers=['Development Status :: 3 - Alpha',
          'Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Security',
          ],
      )