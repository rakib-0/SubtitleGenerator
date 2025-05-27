"""
Setup script for SubtitleGenerator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="subtitle-generator",
    version="1.0.0",
    author="SubtitleGenerator Contributors",
    author_email="",
    description="🎬 Automatically generate and translate subtitles for your videos using AI!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msadeqsirjani/SubtitleGenerator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "flake8>=6.1.0",
            "black>=23.7.0",
            "mypy>=1.5.1",
            "isort>=5.12.0",
            "pre-commit>=3.3.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "subtitle-generator=main:main",
        ],
    },
    keywords="subtitle, video, transcription, translation, whisper, ai, speech-recognition",
    project_urls={
        "Bug Reports": "https://github.com/msadeqsirjani/SubtitleGenerator/issues",
        "Source": "https://github.com/msadeqsirjani/SubtitleGenerator",
        "Documentation": "https://github.com/msadeqsirjani/SubtitleGenerator/wiki",
    },
) 