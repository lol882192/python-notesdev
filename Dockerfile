# Dockerfilee, Image, Container

FROM python:3.12
ADD app.py .
ADD notion_AI_agent.py .

RUN pip install requests flask llama-index llama-index-core llama-index-llms-ollama llama-index-llmms-openai

CMD ["python", "./app.py"]

