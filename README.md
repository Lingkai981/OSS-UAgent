# LLM-based usability evaluation

## Overview
This project is a LLM-based usability evaluation framework including an automated code generator and a code evaluator based on large language models (LLMs), supporting multiple graph analysis platforms and common algorithm implementations. The framework uses Retrieval-Augmented Generation (RAG) technology combined with platform API specifications to generate algorithm implementation code that meets specific platform requirements, and provides multi-dimensional code quality evaluation.

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