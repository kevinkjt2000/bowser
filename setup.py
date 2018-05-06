from setuptools import setup

if __name__ == '__main__':
    setup(
        name='bowser',
        packages=['bowser'],
        entry_points={
            'console_scripts': [
                'bowser = bowser.main:main',
            ]
        },
        use_scm_version=True,
    )
