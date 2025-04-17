from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_ollama import ChatOllama
from e2b_code_interpreter import Sandbox
import os

# Define your tool
@tool
def execute_python_with_ufc_data(code: str):
    """Execute python code to analyze UFC fighter data."""
    with Sandbox() as sandbox:
        # Upload the fighter data to the sandbox
        with open("data/fighter_info.csv", "r") as f:
            csv_content = f.read()
        
        # Create the file in the sandbox
        sandbox.run_code(f"""
        with open("/fighter_info.csv", "w") as f:
            f.write('''{csv_content}''')
        """)
        
        # Run the analysis code
        execution = sandbox.run_code(code)
        return execution.text

# Define system prompt
system_prompt = """You are a Python data analyst expert. Generate code to analyze 
UFC fighter data from /fighter_info.csv with columns: Fighter, Nationality, Wins, Losses.
Only respond with executable Python code, no explanations or markdown."""

# Create the agent
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

tools = [execute_python_with_ufc_data]
llm = ChatOllama(model="mistral:7b")
# llm = ChatOllama(model="mistral:7b-instruct")
# llm = ChatOllama(model="llama3.1:latest")
# llm = ChatOllama(model="cogito:8b")
# llm = ChatOllama(model="deepseek-r1:7b")
# llm = ChatOllama(model="qwen2.5:latest")
# llm = ChatOllama(model="qwq:32b")

agent = create_tool_calling_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Run the agent
query = """Find the top 5 nationalities with the most fighters and calculate 
the average win-loss ratio across all fighters."""
result = agent_executor.invoke({"input": query})
print(result["output"])