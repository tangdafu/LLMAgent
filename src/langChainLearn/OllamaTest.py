from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate


def main():
	llm=ChatOllama(model="qwen3:4b", base_url="http://localhost:11434")
	messages = [
		{"role": "user", "content": "请告诉我一些关于人工智能的基础知识。"}
	]
	messages = [
		SystemMessage("Translate the following from English into Chinese，用中文回答"),
		HumanMessage("hi!"),
	]
	# part 1
	# invoke 直接输出整个结果，流式
	# response = llm.invoke(messages)
	# print(response)

	# part 2
	# stream 打印
	# for token in llm.stream(messages):
	# 	print(token.content)

	# part 3
	system_template = "Translate the following from English into {language}"
	prompt_template = ChatPromptTemplate.from_messages(
		[("system", system_template), ("user", "{text}")]
	)

	prompt = prompt_template.invoke({"language": "Chinese", "text": "hello world!"})

	response = llm.invoke(prompt)
	print(response.content)

if __name__ == '__main__':
	main()
