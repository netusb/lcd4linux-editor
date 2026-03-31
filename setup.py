from setuptools import setup, find_packages

setup(
    name="lcd4linux-editor",
    version="1.0.0",
    description="Visual editor for lcd4linux configuration, designed for AX206 displays",
    author="LCD4Linux Editor Team",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "tkinter",
    ],
    entry_points={
        "console_scripts": [
            "lcd4linux-editor=lcd4linux_editor.src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Hardware",
    ],
)
