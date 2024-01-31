from setuptools import setup, find_packages

setup(
    name='harmony_scope',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool for analyzing Spotify playlists using AI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/HarmonyLens',
    packages=find_packages(),
    install_requires=[
        'spotipy>=2.19.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)
