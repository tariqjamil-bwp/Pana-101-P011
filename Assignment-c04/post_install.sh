#!/bin/bash
set -e

# Install basicsr patched (avoids C++ CUDA extension build and git-hash hang)
BASICSR_DIR=/tmp/basicsr
rm -rf "$BASICSR_DIR"
git clone --depth 1 --branch v1.4.2 https://github.com/xinntao/BasicSR.git "$BASICSR_DIR"

# Patch setup.py: remove write_version_py, simplify get_version, remove C ext deps
cat > "$BASICSR_DIR/setup.py" << 'PYEOF'
#!/usr/bin/env python
from setuptools import find_packages, setup

def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

def get_version():
    with open('VERSION') as f:
        return f.read().strip()

def get_requirements(filename='requirements.txt'):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == '__main__':
    setup(
        name='basicsr',
        version=get_version(),
        description='Open Source Image and Video Super-Resolution Toolbox',
        long_description=readme(),
        long_description_content_type='text/markdown',
        author='Xintao Wang',
        author_email='xintao.wang@outlook.com',
        keywords='computer vision, restoration, super resolution',
        url='https://github.com/xinntao/BasicSR',
        include_package_data=True,
        packages=find_packages(exclude=('options', 'datasets', 'experiments', 'results', 'tb_logger', 'wandb')),
        license='Apache License 2.0',
        setup_requires=['numpy'],
        install_requires=get_requirements(),
        ext_modules=[],
        zip_safe=False,
    )
PYEOF

cd "$BASICSR_DIR"
pip install --no-deps .

# Install AI upscaling & face restoration packages
pip install --no-deps realesrgan gfpgan facexlib
