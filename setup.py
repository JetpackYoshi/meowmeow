from setuptools import setup, find_packages

setup(
    name="nyanpy",
    version="0.1.1",
    description="",
    author="Yoshika Govender",
    author_email="yoshi.govender@gmail.com",
    url="https://github.com/JetpackYoshi/meowmeowutils",
    packages=find_packages(where="src"),  # Find all packages under the src directory
    package_dir={"": "src"},  # Tell setuptools that your packages are under `src/`
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="file tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)