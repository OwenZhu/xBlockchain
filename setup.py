from setuptools import setup

setup(
    name="xBlockchain",
    version="1.0",
    description="Toy Block Chain",
    author="Owen ZHU",
    packages=["xblockchain"],
    package_dir={"": "src"},
    python_requires=">=3.9, <4",
    entry_points={
        'console_scripts': [
            'xblockchain-server-run = xblockchain.cmd:start_server'
        ],
    },
    install_requires=[
        "fastapi==0.79.0",
        "uvicorn==0.18.2",
        "pydantic~=1.9.1",
        "httpx==0.23.0"
    ]
)
