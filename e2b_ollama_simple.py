import os
import ollama
from e2b_code_interpreter import Sandbox
import re

# Define our query for UFC data analysis
query = """
I need Python code to analyze UFC fighter data from the CSV file '/fighter_info.csv'.
The CSV contains fighter information with the following columns:
- Fighter: name of the fighter
- Nationality: country of origin 
- Wins: number of wins (integer)
- Losses: number of losses (integer)

Please create code that:
1. Finds the top 5 nationalities with the most fighters
2. Calculates the average win-loss ratio across all fighters, where win-loss ratio is Wins/(Wins+Losses)
   When calculating the ratio, handle potential division by zero errors appropriately.
   Use numpy for handling NaN values (import numpy as np and use np.nan)

Format the results clearly with proper labels.
"""

# Define system prompt to get code-only responses
system_prompt = """
You are a Python data analyst expert. Generate ONLY Python code to solve the problem.
The user has access to pandas, numpy, and other data science libraries.
Respond with ONLY executable Python code, no explanations or markdown formatting.
DO NOT include backticks (```) in your response.
"""

# Send the query to Ollama to generate Python code
response = ollama.chat(
    model="mistral:7b",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": query
        }
    ]
)

# Extract the code from the response
code = response['message']['content']

# Clean the code - remove markdown formatting if present
code = re.sub(r'^```python\s*', '', code)  # Remove opening ```python
code = re.sub(r'```\s*$', '', code)        # Remove closing ```

# Print the generated code for reference
print("Generated Python code:")
print("-" * 40)
print(code)
print("-" * 40)

# Execute the code in E2B Sandbox
print("\nExecuting code in E2B Sandbox...\n")
with Sandbox() as sandbox:
    # Read the CSV file
    with open("data/fighter_info.csv", "r") as f:
        csv_content = f.read()
    
    # Create the file in the sandbox
    sandbox.run_code(f"""
with open("/fighter_info.csv", "w") as f:
    f.write('''{csv_content}''')
""")
    
    # Run the code
    execution = sandbox.run_code(code)
    
    # Get the result
    result = ""
    if execution.error:
        result = f"Error: {execution.error.name}: {execution.error.value}\n{execution.error.traceback}"
    else:
        # Check for results (for charts, tables, etc.)
        result_idx = 0
        for result_item in execution.results:
            if hasattr(result_item, 'png') and result_item.png:
                # If we had PNG content, we could save it
                # with open(f'chart-{result_idx}.png', 'wb') as f:
                #     f.write(base64.b64decode(result_item.png))
                result += f"[Generated chart {result_idx}]\n"
                result_idx += 1
        
        # If no result items with specific content, use stdout
        if not result and execution.logs and execution.logs.stdout:
            result = execution.logs.stdout

# Save both the code and results
with open("output/ufc_basic1_ollama_e2b_output.txt", "w") as f:
    f.write("GENERATED CODE:\n\n")
    f.write(code)
    f.write("\n\nRESULTS:\n\n")
    f.write(str(result))  # Convert to string regardless of type

# Print the results
print("\nResults:")
print("-" * 40)
print(result)
print("-" * 40) 