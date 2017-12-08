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

setup_requirements = [
    'setuptools_scm',
]

setup(
    install_requires=requirements,
    extras_require={'dev': test_requirements},
    setup_requires=setup_requirements,
    packages=['src'],
    use_scm_version=True,
)
