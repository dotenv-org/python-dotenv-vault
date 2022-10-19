import os
import sys
from setuptools import setup, find_packages

src = {}
dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(dir, "src/dotenv", "__version__.py"), "r") as f:
    exec(f.read(), src)

with open("README.md", "r") as f:
    readme = f.read()

# 'setup.py publish' shortcut.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist")
    os.system(f"twine upload dist/python-dotenv-vault-{src['__version__']}.tar.gz")
    sys.exit()

setup(
    name='python-dotenv-vault',
    description=src['__description__'],
    version=src['__version__'],
    license=src['__license__'],
    author=src['__author__'],
    author_email=src['__author_email__'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url=src['__url__'],
    keywords=[
    'environment',    
    'environment variables',
    'deployments',
    'settings',
    'env',
    'dotenv',
    'configurations',
    'python',
    'dotenv-vault'
    ],
    install_requires=[],
)