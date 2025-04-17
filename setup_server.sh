#!/bin/bash

echo "⬇️ Installing Claude Code CLI..."
npm install -g claude-code

echo "🚀 Installing Claude Code MCP servers..."

echo "📁 Installing Filesystem MCP..."
claude mcp add filesystem --scope user -- npx -y modelcontextprotocolserverfilesystem ./data

# echo "🧠 Installing SQLite MCP..."
# mkdir mcps
# git clone https://github.com/modelcontextprotocol/servers.git mcps/
# claude mcp add sqlite --scope user -- npx -y ./mcps/sqlite --dbpath ./data/ufc_database.db

echo "✅ Verifying..."
claude mcp list

# # Sequential Thinking MCP
# echo "📊 Setting up Sequential Thinking Claude MCP..."
# claude mcp add sequentialthinking --scope user -- npx -y modelcontextprotocolserversequentialthinking

# # Filesystem Access
# echo "📁 Setting up Filesystem Access Claude MCP..."
# claude mcp add filesystem --scope user -- npx -y modelcontextprotocolserverfilesystem ~/Documents ~/Desktop ~/Downloads ~/Projects

# # Puppeteer Browser Automation
# echo "🌐 Setting up Puppeteer Browser Automation..."
# claude mcp add puppeteer --scope user -- npx -y modelcontextprotocolserverpuppeteer

# # Web Fetching
# echo "🔍 Setting up Web Fetching..."
# claude mcp add fetch --scope user -- npx -y kazuphmcpfetch

# # Verify
# echo "✅ Verifying installation..."
# claude mcp list

# echo "🎉 Basic MCP servers installed successfully!"
