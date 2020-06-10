from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

print(find_packages())

setup(
    install_requires=[
        "boto3==1.13.26",
        "botocore==1.16.26",
        "click==7.1.2",
        "docutils==0.15.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "jmespath==0.10.0; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "ruamel-yaml==0.16.10",
        "ruamel.yaml.clib==0.2.0; python_version < '3.9' and platform_python_implementation == 'CPython'",
        "s3transfer==0.3.3",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.25.9; python_version != '3.4'",
    ],
    name="croudtech-helm-helper",  # Replace with your own username
    version="0.0.1",
    author="Jim Robinson",
    author_email="jscrobinson@gmail.com",
    description="Helm utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CroudTech/devops-python-package-deployment-worker",
    packages=["croudtech_helm_helper"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["croudtech-helm-helper=croudtech_helm_helper.cli:main"],
    },
)
