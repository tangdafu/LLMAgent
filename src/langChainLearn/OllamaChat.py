from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

model = ChatOllama(model="qwen3:4b", base_url="http://localhost:11434")
model.invoke([HumanMessage(content="Hi! I'm Bob")])


def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}


# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

query = "Hi! I'm Bob."

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()  # output contains all messages in state


query = "What's my name?"

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()
