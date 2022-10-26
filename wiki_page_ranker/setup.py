from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    description = readme.read()

with open("requirements.txt", "r", encoding="utf-8") as reqs:
    requirements = reqs.read()


setup(
    name='wikipedia_page_ranker',
    version='1.0',
    author='Uladzimir Fiodarau',
    author_email='ufiodarau@gmail.com',
    description='A page ranker for Wikipedia',
    long_description=description,
    packages=find_packages(),
    package_data={'': ['*.txt']
                  },
    install_requires=[requirements],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
