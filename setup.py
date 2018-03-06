from distutils.core import setup

REQUIREMENTS = {
    'extras': {
        'ci': [
            'codecov',
        ],
        'test': [
            'asynctest',
            'pytest',
            'pytest-cov',
            'pytest-socket',
        ],
    },
    'install': [
        'discord.py',
        'mcstatus',
    ],
    'setup': [
        'setuptools_scm',
    ],
}

setup(
    name='bowser',
    install_requires=REQUIREMENTS['install'],
    extras_require=REQUIREMENTS['extras'],
    setup_requires=REQUIREMENTS['setup'],
    packages=['bowser'],
    scripts=['scripts/bowser-bot'],
    use_scm_version=True,
)
