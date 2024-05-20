

import os

from setuptools import setup, find_packages

# get file path
file_path = os.path.dirname(os.path.realpath(__file__))

if os.path.exists(f'{file_path}/packages'):
    os.system(f'rm -rf {file_path}/packages')
else :    
    os.system(f'cd {file_path} && mkdir packages')
## clone uix
os.system(f'cd {file_path}/packages && git clone https://github.com/aitsis/uix.git')
os.system(f'cd {file_path}/packages/uix && pip install -e .')

## clone uix-components
os.system(f'cd {file_path}/packages && git clone https://github.com/aitsis/uix-components.git')
os.system(f'cd {file_path}/packages/uix-components && pip install -e .')

os.system(f'(cd {file_path} | pip install -r requirements.txt)')