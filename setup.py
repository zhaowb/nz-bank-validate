import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nz-bank-validate",
    version="1.0.0",
    author="Wenbo Zhao",
    author_email="zhaowb@gmail.com",
    description="Validates account numbers for New Zealand banks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhaowb/nz-bank-validate.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
    py_modules=['nz_bank_validate']
)
