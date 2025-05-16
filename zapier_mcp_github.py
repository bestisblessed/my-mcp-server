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

        # 1. github_find_organization
        print("Testing github_find_organization...")
        org_result = await client.call_tool(
            "github_find_organization",
            {
                "name": "github",  # organization name
                "instructions": "Find info about the organization github",
                "auth": {
                    "accountId": 11531798,
                    "customuserId": 11531798
                }
            }
        )
        print("Organization result:")
        print(json.dumps(json.loads(org_result[0].text), indent=2))

        # 2. github_find_repository
        print("Testing github_find_repository...")
        repo_result = await client.call_tool(
            "github_find_repository",
            {
                "owner": "bestisblessed",
                "repo": "bestisblessed",  # replace with actual repo name
                "instructions": "Find info about the repository bestisblessed",
                "auth": {
                    "accountId": 11531798,
                    "customuserId": 11531798
                }
            }
        )
        print("Repository result:")
        print(json.dumps(json.loads(repo_result[0].text), indent=2))

        # 3. github_find_user
        print("Testing github_find_user...")
        user_result = await client.call_tool(
            "github_find_user",
            {
                "desired_username": "bestisblessed",
                "instructions": "Find info about the user bestisblessed",
                "auth": {
                    "accountId": 11531798,
                    "customuserId": 11531798
                }
            }
        )
        print("User result:")
        print(json.dumps(json.loads(user_result[0].text), indent=2))

    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())