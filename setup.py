from setuptools import setup, find_packages

setup(
    name="music-sync",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "spotipy",
        "ytmusicapi",
        "python-dotenv",
        "sqlalchemy",
        "alembic",
    ],
)
