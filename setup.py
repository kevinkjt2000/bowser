from setuptools import setup

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
        'retrying',
    ],
    'setup': [
        'setuptools_scm',
    ],
}

if __name__ == '__main__':
    setup(
        name='bowser',
        install_requires=REQUIREMENTS['install'],
        extras_require=REQUIREMENTS['extras'],
        setup_requires=REQUIREMENTS['setup'],
        packages=['bowser'],
        entry_points={
            'console_scripts': [
                'bowser = bowser.main:main',
            ]
        },
        use_scm_version=True,
    )
