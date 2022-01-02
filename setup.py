"""**Setup interface**

1. Approach to the source code with `python setup.py 'COMMAND'`
2. Append the 'COMMAND' adding `cmdclass` in `setup()`

----
"""

from setuptools import find_packages, setup
from setuptools import Command
from subprocess import run


### Long description is in 'README.md'
with open("README.md", "r") as f:
    long_description = f.read()


### Permitted commands
class MainCommand:
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass

    @staticmethod
    def run_main(option):
        run(["python", "main.py", f"--CMD {option}"], cwd="trading_system")


class Run(MainCommand, Command):
    description = "Run /trading_system/main.py --CMD run"
    def run(self):
        super().run_main('run')

class Clean(MainCommand, Command):
    description = "Run /trading_system/main.py --CMD clean"
    def run(self):
        super().run_main('clean')


### Setup summary
setup(
    name="trading-system",
    version="0.0.1",
    author="Dongjin Yoon",
    author_email="djyoon0223@gmail.com",
    description="자동 매매 시스템",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djy-git/trading-system",
    packages=find_packages(),  # `requirements.txt` is preferred
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        # "Environment :: GPU :: NVIDIA CUDA :: 10.2",
    ],
    python_requires=">=3.8",
    cmdclass={
        "run"  : Run,
        "clean": Clean,
    }
)
