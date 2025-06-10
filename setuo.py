from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "A sassy sentiment analysis bot with quote generation"

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "textblob>=0.17.1",
            "vaderSentiment>=3.3.2",
            "openai>=1.3.0",
            "python-dotenv>=1.0.0",
            "requests>=2.31.0",
            "nltk>=3.8.1",
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
        ]

setup(
    name="sentiment-bot",
    version="1.0.0",
    description="A sassy sentiment analysis bot with quote generation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/sentiment-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    install_requires=read_requirements(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "sentiment-bot=main:main",
            "sentiment-test=main:test_mode",
            "sentiment-interactive=utils.helpers:interactive_mood_analyzer",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="sentiment analysis, nlp, chatbot, quotes, AI, GPT, TextBlob, VADER",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/sentiment-bot/issues",
        "Source": "https://github.com/yourusername/sentiment-bot",
        "Documentation": "https://github.com/yourusername/sentiment-bot/blob/main/README.md",
    },
)