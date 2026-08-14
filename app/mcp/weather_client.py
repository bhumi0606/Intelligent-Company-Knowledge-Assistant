import asyncio

from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client


# server_params = StdioServerParameters(
#     command="python",
#     args=["-m", "open_meteo_mcp"],
# )

# get current weather tool (stdio)
# async def get_current_weather(city: str):
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:

#             await session.initialize()

#             result = await session.call_tool(
#                 "get_current_weather",
#                 {
#                     'city': city
#                 }
#             )

#             return result

# get current weather tool (stremable)
async def get_current_weather(city: str):
    async with streamable_http_client("http://localhost:8080/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_current_weather",
                {
                    'city': city
                }
            )

            return result
