from setuptools import find_packages, setup
from SlashPaginator import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SlashPaginator",
    license="MIT",
    version=__version__,
    description="Button paginator using discord-py-interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DeltaX",
    author_email="delta@deltax.dev",
    url="https://github.com/DeltaXWizard/ButtonPaginator",
    packages=find_packages(),
    keywords=[
        "discord.py",
        "pagination",
        "button",
        "components",
        "slash",
        "discord_slash_commands",
    ],
    python_requires=">=3.6",
    install_requires=["discord.py", "discord-py-slash-command"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
