from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

print(find_packages())

setup(
    install_requires=[
        "boto3==1.14.3",
        "botocore==1.17.3",
        "certifi==2020.4.5.2",
        "chardet==3.0.4",
        "click==7.1.2",
        "docker==4.2.1",
        "docker-registry-client==0.5.2",
        "docutils==0.15.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "ecdsa==0.13.3",
        "idna==2.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "jmespath==0.10.0; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "jws==0.1.3",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "requests==2.23.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "ruamel.yaml==0.16.10",
        "ruamel.yaml.clib==0.2.0; python_version < '3.9' and platform_python_implementation == 'CPython'",
        "s3transfer==0.3.3",
        "semver==2.10.2",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.26.5; python_version != '3.4'",
        "websocket-client==0.57.0",
    ],
    name="croudtech-helm-helper",  # Replace with your own username
    version="0.0.1",
    author="Jim Robinson",
    author_email="jscrobinson@gmail.com",
    description="Helm utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CroudTech/devops-python-package-deployment-worker",
    packages=["croudtech_helm_helper", "croudtech_helm_helper.docker_tools"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["croudtech-helm-helper=croudtech_helm_helper.cli:cli"],
    },
)
