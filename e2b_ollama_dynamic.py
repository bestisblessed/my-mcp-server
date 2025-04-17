import os
import re
import argparse
import ollama
from e2b_code_interpreter import Sandbox
import pandas as pd
import json

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Analyze UFC fighter data with dynamic questions')
    parser.add_argument('-q', '--question', required=True, help='The question about UFC fighter data')
    parser.add_argument('-m', '--model', default='mistral:7b', help='Ollama model to use (default: mistral:7b)')
    parser.add_argument('-r', '--retries', type=int, default=4, help='Number of retries for error correction (default: 4)')
    return parser.parse_args()

def get_data_info():
    # Load the data
    df = pd.read_csv("data/fighter_info.csv")
    
    # Get basic information
    info = {
        "columns": list(df.columns),
        "num_fighters": len(df),
        "sample_data": df.head(3).to_dict(orient='records'),
        "column_types": {col: str(df[col].dtype) for col in df.columns},
        "has_nulls": {col: bool(df[col].isna().sum() > 0) for col in df.columns},
        # "value_counts": {
        #     "Weight Class": df["Weight Class"].value_counts().to_dict(),
        #     "Nationality": df["Nationality"].value_counts().head(5).to_dict()
        # }
    }
    return info

# Top Weight Classes:
# {json.dumps(data_info['value_counts']['Weight Class'], indent=2)}
# Top Nationalities:
# {json.dumps(data_info['value_counts']['Nationality'], indent=2)}


def get_ai_generated_code(question, model_name):
    """Get code from AI model based on question"""
    # Get data info for context
    data_info = get_data_info()
    
    # Construct the full query with context about the data
    query = f"""
I need Python code to analyze UFC fighter data from the CSV file '/fighter_info.csv'.

Here is information about the dataset:

Column names: {data_info['columns']}

Sample data (first 3 rows):
{json.dumps(data_info['sample_data'], indent=2)}

Dataset has {data_info['num_fighters']} fighters.

Column data types:
{json.dumps(data_info['column_types'], indent=2)}

Columns with null values:
{json.dumps({k: v for k, v in data_info['has_nulls'].items() if v}, indent=2)}

Please answer this question about the data: {question}

Generate Python code that solves this using pandas and other appropriate libraries.
Handle potential errors like division by zero or missing values appropriately.
Format the results clearly with proper labels.
Summarize the results at the end of the code.
"""

    # System prompt that instructs the AI to generate only code
    system_prompt = """
You are a Python data analyst expert. Generate ONLY Python code to solve the problem.
The user has access to pandas, numpy, and other data science libraries.
Respond with ONLY executable Python code, no explanations or markdown formatting.
DO NOT include backticks (```) in your response.
The data file is at '/fighter_info.csv' (with the leading slash).
"""

    # Send the query to Ollama to generate Python code
    print(f"Asking {model_name} to generate code...")
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    
    # Clean the code response more thoroughly
    code = response['message']['content']
    code = re.sub(r'```python\s*', '', code)  # Remove ```python anywhere
    code = re.sub(r'```\s*', '', code)        # Remove ``` anywhere
    return code.strip()  # Strip leading/trailing whitespace

def execute_in_sandbox(code, max_retries=4):
    """Execute code in sandbox with retry logic for errors"""
    retry_count = 0
    
    with Sandbox() as sandbox:
        # Prepare the data file
        with open("data/fighter_info.csv", "r") as f:
            csv_content = f.read()
        
        # Create the file in sandbox
        sandbox.run_code(f"""
with open("/fighter_info.csv", "w") as f:
    f.write('''{csv_content}''')
""")
        
        while retry_count <= max_retries:
            # Run the code
            execution = sandbox.run_code(code)
            
            # Check for errors
            if execution.error:
                error_msg = f"Error: {execution.error.name}: {execution.error.value}\n{execution.error.traceback}"
                print(f"\nExecution error (attempt {retry_count + 1}/{max_retries + 1}):")
                print("-" * 40)
                print(error_msg)
                
                if retry_count < max_retries:
                    # Try to fix the code
                    print(f"\nAttempting to fix the code (retry {retry_count + 1})...")
                    
                    # Get data info for context
                    data_info = get_data_info()
                    
                    fix_query = f"""
The following Python code has an error:
{code}

The error is:
{error_msg}

The CSV file has these columns:
{data_info['columns']}

Please provide a fixed version of this code that works correctly.
Just give the complete fixed code without any explanations.
The data file is at '/fighter_info.csv' (with the leading slash).
"""
                    response = ollama.chat(
                        model="mistral:7b",  # Use mistral for fixes regardless of initial model
                        messages=[
                            {"role": "user", "content": fix_query}
                        ]
                    )
                    
                    # Extract the fixed code with more thorough cleaning
                    fixed_code = response['message']['content']
                    fixed_code = re.sub(r'```python\s*', '', fixed_code)  # Remove ```python anywhere
                    fixed_code = re.sub(r'```\s*', '', fixed_code)        # Remove ``` anywhere
                    fixed_code = fixed_code.strip()  # Ensure no leading/trailing whitespace
                    
                    # Update code for next attempt
                    code = fixed_code
                    print("\nFixed code generated. Trying again...")
                    retry_count += 1
                else:
                    # Max retries reached, return error
                    return error_msg, code
            else:
                # Code executed successfully
                if execution.logs and execution.logs.stdout:
                    result = execution.logs.stdout
                elif hasattr(execution, 'text'):
                    result = execution.text
                else:
                    result = "Execution completed but no output detected."
                    
                return result, code
    
    # This should not be reached under normal circumstances
    return "Unexpected error in execution process", code

def main():
    """Main function to run the analysis"""
    args = parse_arguments()
    
    print(f"\nQuestion: {args.question}")
    print(f"Using model: {args.model}")
    print(f"Maximum retries: {args.retries}")
    print("-" * 50)
    
    # Generate code based on the question
    code = get_ai_generated_code(args.question, args.model)
    
    # Display the generated code
    print("\nGenerated Python code:")
    print("-" * 50)
    print(code)
    print("-" * 50)
    
    # Execute the code
    print("\nExecuting code in sandbox...\n")
    result, final_code = execute_in_sandbox(code, args.retries)
    
    # Clean up the results - just add this part
    if isinstance(result, list):
        # If it's actually a list object, convert to string
        cleaned_result = '\n'.join(str(item) for item in result)
    elif isinstance(result, str) and result.startswith('[') and result.endswith(']'):
        # Simple string cleanup for list-like results
        cleaned_result = result.strip('[]"\' ')  # Remove brackets, quotes
        cleaned_result = cleaned_result.replace('\\n', '\n')  # Convert escape sequences
        cleaned_result = cleaned_result.replace('\\t', '\t')  # Convert tabs
    else:
        cleaned_result = str(result)  # Ensure it's a string
    
    # Save results
    output_file = f"output/ufc_dynamic_output.txt"
    with open(output_file, "w") as f:
        f.write(f"QUESTION:\n{args.question}\n\n")
        f.write("FINAL CODE:\n\n")
        f.write(final_code)
        f.write("\n\nRESULTS:\n\n")
        f.write(cleaned_result)  # Now we're sure this is a string
    
    # Display results
    print("\nResults:")
    print("-" * 50)
    print(cleaned_result)
    print("-" * 50)
    print(f"\nOutput saved to {output_file}")

if __name__ == "__main__":
    main()