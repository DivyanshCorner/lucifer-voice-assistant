# Contributing

Thanks for taking the time to help improve Lucifer.

## Reporting a problem

Open an issue and include:

- your Windows and Python versions
- the command you said and what you expected
- the full error message, if there was one

Please remove any API keys from logs before pasting them.

## Sending a change

1. Fork the repository and create a branch for your change.
2. Keep the change focused. One feature or fix per pull request.
3. Follow PEP 8 and keep new commands in their own small function.
4. Never hard-code keys or personal paths. Read them from environment variables and document them in `.env.example`.
5. Describe what you changed and how you tried it out in the pull request.

## Local setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python lucifer.py
```
