#!/bin/bash

# Default settings
DEFAULT_MODEL="mistral:7b"
DEFAULT_RETRIES=3

# Function to display usage information
show_usage() {
    echo "UFC Fighter Data Analysis Script"
    echo "--------------------------------"
    echo "Usage: ./run_dynamic_simple.sh \"Your question about UFC fighter data\""
    echo "   or: ./run_dynamic_simple.sh -m model_name \"Your question about UFC fighter data\""
    echo "   or: ./run_dynamic_simple.sh -m model_name -r retry_count \"Your question about UFC fighter data\""
    echo ""
    echo "Options:"
    echo "  -m MODEL    Specify the Ollama model to use (default: $DEFAULT_MODEL)"
    echo "  -r RETRIES  Number of retries for fixing errors (default: $DEFAULT_RETRIES)"
    echo "  -h, --help  Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_dynamic_simple.sh \"Who are the top 5 fighters with the most KO wins?\""
    echo "  ./run_dynamic_simple.sh -m llama2 \"Which nationality has the highest win percentage?\""
    echo "  ./run_dynamic_simple.sh -m mistral:7b -r 6 \"Tell me about Alex Volkanovski\""
    echo ""
    echo "Available models depend on your Ollama installation."
}

# Process arguments
MODEL=$DEFAULT_MODEL
RETRIES=$DEFAULT_RETRIES
QUESTION=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_usage
            exit 0
            ;;
        -m)
            if [[ $# -lt 2 ]]; then
                echo "Error: Missing model name after -m"
                show_usage
                exit 1
            fi
            MODEL="$2"
            shift 2
            ;;
        -r)
            if [[ $# -lt 2 ]]; then
                echo "Error: Missing retry count after -r"
                show_usage
                exit 1
            fi
            RETRIES="$2"
            shift 2
            ;;
        *)
            # If we hit a non-option, the rest is the question
            QUESTION="$*"
            break
            ;;
    esac
done

# Check if the question is provided
if [ -z "$QUESTION" ]; then
    echo "Error: No question provided."
    show_usage
    exit 1
fi

# Run the Python script with the provided arguments
echo "Analyzing: $QUESTION"
echo "Using model: $MODEL"
echo "Maximum retries: $RETRIES"
echo "--------------------------------"

python e2b_ollama_dynamic.py -q "$QUESTION" -m "$MODEL" -r "$RETRIES" 