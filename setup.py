import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vqe_playground_006",
    version="0.0.1",
    author="James L. Weaver",
    author_email="james.l.weaver@gmail.com",
    description="Variational Quantum Eigensolver Playground",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JavaFXpert/vqe-playground",
    packages=setuptools.find_packages(),
    install_requires=[
        'pygame',
        'networkx',
        #'qiskit',  # not including for now, because of hard scikit learn reqirement
        #'qiskit_aqua',
    ],
    package_data={
        'vqe_playground.utils': ['**/*.png'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'vqe-playground = vqe_playground.command_line:main',
        ],
    },
)
