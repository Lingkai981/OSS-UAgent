# OSS-UAgent: An Agent-based Usability Evaluation Framework for Open Source Software

## Quick Start

### Environment Setup
```shell
python -m venv venv                                             
source venv/bin/activate
pip install flask flask-cors langchain openai faiss-cpu langchain-openai pydantic langchain_community
```
#### Set the OpenAI API key as an environment variable:
Open your terminal and add the following line to your shell configuration file (.bashrc, .zshrc, etc.):
```shell
export OPENAI_API_KEY="your-api-key-here"
```
Reload the shell configuration:
```shell
source ~/.bashrc   # If you use bash
source ~/.zshrc    # If you use zsh
```
### Running the Program
```shell
python3 main.py
```
Start a new terminal
```shell
cd app/
npm start
```