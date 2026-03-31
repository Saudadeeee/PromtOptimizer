from setuptools import setup, find_packages

setup(
    name='po-cli',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'typer',
        'rich',
        'pyperclip',
        'litellm',
        'python-dotenv',
        'tiktoken',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'po=po_cli.main:app',
        ],
    },
    author="You",
    description="Prompt Optimizer CLI",
)
