from distutils.core import setup

setup(
    name='PocketPy',
    version='0.1.1',
    author='Richard Delaney',
    author_email='richdel1991@gmail.com',
    packages=['pocketpy', 'pocketpy.test'],
    scripts=['bin/operators.py', 'bin/pocket_ticker.py'],
    url='http://pypi.python.org/pypi/PocketPy',
    license='LICENSE.txt',
    description='A python wrapper and some scripts for communication with pocket api',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests==2.28",
    ],
)
