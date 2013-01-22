from distutils.core import setup

setup(
    name='PocketPy',
    version='0.1.0',
    author='Richard Delaney',
    author_email='richdel1991@gmail.com',
    packages=['pocketpy', 'pocketpy.test'],
    scripts=['bin/comments_apply.py', 'bin/operators.py', 'bin/pocket_ticker.py'],
    url='http://pypi.python.org/pypi/HNComments/',
    license='LICENSE.txt',
    description='A python wrapper and some scripts for communication with pocket api',
    long_description=open('README.txt').read(),
    install_requires=[
        "HNComments==0.1.1",
        "argparse==1.2.1",
        "requests==1.0.4",
        "wsgiref==0.1.2",
    ],
)
