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

        print("Scraping DraftKings UFC odds page...")
        result = await client.call_tool(
            "scrapingant_scrape_page",
            {
                "url": "https://sportsbook.draftkings.com/leagues/mma/ufc",
                "instructions": "Scrape the UFC odds page from DraftKings Sportsbook"
            }
        )
        print("Scraped page result:")
        print(json.dumps(json.loads(result[0].text), indent=2))

    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())