from distutils.core import setup

requirements = [
    'discord.py',
    'mcstatus',
]

test_requirements = [
    'asynctest',
    'pytest',
    'pytest-cov',
    'pytest-socket',
    'python-coveralls',
]

setup(
    install_requires=requirements,
    extras_require={'dev': test_requirements},
    packages=['src'],
)
