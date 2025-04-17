#!/bin/bash

# export ANTHROPIC_MODEL="claude-3-sonnet-20240229"
export ANTHROPIC_MODEL="claude-3-5-haiku-20241022"
# export CLAUDE_AUTO_APPROVE_TOOLS="Bash:*,ReadFile:*,WriteFile:*,ListDir:*,Edit:*,Bash:python*,Bash:pandas*,Bash:pip*,Bash:matplotlib*,Bash:numpy*,Bash:scipy*,Bash:scikit-learn*,Bash:sklearn*,Bash:seaborn*,Bash:jupyter*,Bash:cat*,Bash:ls*,Bash:head*,Bash:tail*,Bash:grep*,Bash:awk*,Bash:sed*"
export CLAUDE_AUTO_APPROVE_TOOLS="true"  # This grants all permissions

# Define the prompt
query="What are the top 5 nationalities with the most fighters in the UFC dataset? Print the total number of eacb country."
# query="Also, calculate and show the average win-loss ratio across all fighters"

# claude -p "$query"
claude -p "$query"
#  --output-format text | tee output/mcp_server_output.txt