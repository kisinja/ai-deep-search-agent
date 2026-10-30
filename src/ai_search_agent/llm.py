from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3.5:2b",
    temperature=0,
    reasoning=False,  # turns thinking off
    num_predict=300,
)