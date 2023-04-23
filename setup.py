from setuptools import setup, find_packages

setup(
    name='scCMGAN',
    version='0.1',
    packages=find_packages(),
    install_requires = [
        "ctgan",
        "pickle-mixin",
        "numpy"
    ]
)

# "sklearn",
