# Demo Scripts for Class Walkthrough

This folder contains quick Python demos for these exercises:

- Exercise 3: Create a generative AI chat app
- Exercise 4: Create a generative AI chat app (Foundry SDK)
- Exercise 4A: Create a generative AI app that uses tools

## 1) Setup

```powershell
cd demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2) Configure environment

Edit `.env` with your Azure values.

## 3) Run demos

```powershell
python exercise3_chat_app_demo.py
python exercise4_foundry_sdk_demo.py
python exercise4a_tools_demo.py
```

## Notes

- Exercise 3 and 4A scripts use Azure OpenAI chat completions.
- Exercise 4 script uses Azure AI Foundry Inference SDK (`azure-ai-inference`).
- Keep model names and endpoints aligned with your provisioned resources.
