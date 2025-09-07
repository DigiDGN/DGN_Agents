from setuptools import setup

setup(
    name="DGN_Agents",
    packages=["DGN_Agents"],  # this must be the same as the name above
    version="0.2.2",
    description="A Python package for easily interfacing with chat apps, with robust features and minimal code complexity.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="The Pacifist Anarchist",
    author_email="dylan.griffin138@gmail.com",
    url="https://github.com/DigiDGN/DGN_Agents",
    keywords=["chatgpt", "openai", "text generation", "ai"],
    classifiers=[],
    license="MIT",
    entry_points={
    "console_scripts": ["DGN_Agents=DGN_Agents.cli:interactive_chat"]
    },
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0",
        "fire>=0.3.0",
        "httpx>=0.24.1",
        "python-dotenv>=1.0.0",
        "orjson>=3.9.0",
        "rich>=13.4.1",
        "python-dateutil>=2.8.2",
    ],
)
