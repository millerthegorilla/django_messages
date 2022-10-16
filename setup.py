import os

from setuptools import find_packages, setup

# Optional project description in README.md:

current_directory = os.path.dirname(os.path.abspath(__file__))

try:

    with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:

        long_description = f.read()

except Exception:

    long_description = "django_messages adds basic messaging."

setup(
    # Project name:
    name="django-messages",
    # Packages to include in the distribution:
    packages=find_packages(","),
    # Project version number:
    version="0.0.1",
    # List a license for the project, eg. MIT License
    license="MIT",
    # Short description of your library:
    description="A simple django app that adds basic messaging",
    # Long description of your library:
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Your name:
    author="James Miller",
    # Your email address:
    author_email="jamesstewartmiller@gmail.com",
    # Link to your github repository or website:
    url="https://github.com/millerthegorilla/django_messages",
    # Download Link from where the project can be downloaded from:
    download_url="https://github.com/millerthegorilla/django_messages",
    # List of keywords:
    keywords=["django", "django_messages", "messages app"],
    # List project dependencies:
    install_requires=[
        "django>=4.0.1",
        "django-q>=1.3.9",
        "bleach>=5.0.1",
        "django-crispy-forms>=1.14.0",
        "crispy-bootstrap5>=0.7",
        "django-redis>=5.2.0",
    ],
    # https://pypi.org/classifiers/
    classifiers=[
        "DevelopmentStatus::2-Pre-Alpha",
        "Framework::Django CMS",
        "Framework::Django::4.0",
    ],
)
