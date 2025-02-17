"""Setup file for the package"""
from setuptools import setup

setup(
    name='sib',
    version='1.0',
    packages=['sib/literature'],
    install_requires=['requests', 'openai'],
)
