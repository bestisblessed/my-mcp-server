import asyncio
import json
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

server_url = "https://mcp.zapier.com/api/mcp/s/ZmI1YjNkMTUtYTRiYS00Yjk5LTg5OTktNmI3NzIwMTRlNjFmOjM3OTk5NmQ5LTVlOWYtNGM2YS1hM2ZjLWRkY2ZlZTZjYTMwNQ==/mcp"
transport = StreamableHttpTransport(server_url)
client = Client(transport=transport)

async def main():
    print("Connecting to MCP server...")
    async with client:
        print(f"Client connected: {client.is_connected()}")
        
        # Print available tools
        print("Fetching available tools...")
        tools = await client.list_tools()
        print(f"Available tools: {json.dumps([t.name for t in tools], indent=2)}")
        
        ## Call a specific tool with prompt
        #print("Calling github_check_organization_membership...")
        #result = await client.call_tool(
        #    "github_check_organization_membership",
        #    {
        #        "instructions": "Execute the GitHub: Check Organization Membership tool with the following parameters",
        #        "org": "example-string",
        #        "username": "example-string",
        #    },
        #)
        #json_result = json.loads(result[0].text)
        #print(
        #    f"\ngithub_check_organization_membership result:\n{json.dumps(json_result, indent=2)}"
        #)
    print("Example completed")
    
if __name__ == "__main__":
    asyncio.run(main())

