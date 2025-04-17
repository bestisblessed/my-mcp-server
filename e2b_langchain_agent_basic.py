from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_ollama import ChatOllama  # Changed from langchain_openai
from e2b_code_interpreter import Sandbox

system_prompt = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
prompt = "Calculate how many r's are in the word 'strawberry'"

# Define the tool
@tool
def execute_python(code: str):
    """Execute python code in a Jupyter notebook."""
    with Sandbox() as sandbox:
        execution = sandbox.run_code(code)
        return execution.text

# Define LangChain components
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

tools = [execute_python]
llm = ChatOllama(
    model="llama3.1:latest",  # Using a model that supports tool calling
    # model="mistral:7b",
    # model="cogito:8b",
    # model="deepseek-r1:8b",
    # temperature=0.0
)

agent = create_tool_calling_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent
result = agent_executor.invoke({"input": prompt})
print(result["output"])  # Print only the output





# from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from e2b_code_interpreter import Sandbox

# # Create sandbox
# sbx = Sandbox()

# # Configure LLM
# llm = ChatOllama(model="llama3.1:latest", temperature=0.1)
# prompt_template = ChatPromptTemplate.from_messages([
#     ("system", """
# You are a data analyst assistant that can execute Python code. 
# When asked to analyze data, respond with Python code that uses pandas for analysis.
# Only provide the code, no explanations."""),
#     ("human", "{input}")
# ])
# output_parser = StrOutputParser()

# # Create the chain
# chain = prompt_template | llm | output_parser 

# # Generate code for data analysis
# query = "Load the fighter_info.csv file from the data directory and provide a summary of the dataset, including basic statistics and the first few rows."
# code = chain.invoke({"input": query})

# # Execute code in E2B Sandbox
# with Sandbox() as sandbox:
#     with open("data/fighter_info.csv", "rb") as file:
#         # content = file.read()  # Read the file content
#         sbx.files.write("/home/user/my-file", file)
#     execution = sandbox.run_code(code)
#     result = execution.text
    
# print(result)


# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.tools import tool
# from langchain.agents import create_tool_calling_agent, AgentExecutor
# from langchain_openai import ChatOpenAI
# from e2b_code_interpreter import Sandbox

# system_prompt = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
# prompt = "Calculate how many r's are in the word 'strawberry'"

# # Define the tool
# @tool
# def execute_python(code: str):
#     """
#     Execute python code in a Jupyter notebook.
#     """
#     with Sandbox() as sandbox:
#         execution = sandbox.run_code(code)
#         return execution.text

# # Define LangChain components
# prompt_template = ChatPromptTemplate.from_messages([
#     ("system", system_prompt),
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}"),
# ])

# tools = [execute_python]
# llm = ChatOpenAI(
#     model="llama3.1:latest",
#     temperature=0
# )
# agent = create_tool_calling_agent(llm, tools, prompt_template)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# # Run the agent
# agent_executor.invoke({"input": prompt})



