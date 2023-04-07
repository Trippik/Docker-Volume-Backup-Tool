from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="Docker-Volume-Backup-Tool",
    version="1.0",
    author="Cameron Trippick",
    install_requires=requirements,
    packages=['docker_volume_backup', 'docker_volume_backup.lib'],
    entry_points={
        'console_scripts': [
            'Docker-Volume-Backup-Tool = docker_volume_backup.app:main',
        ]
    }
)