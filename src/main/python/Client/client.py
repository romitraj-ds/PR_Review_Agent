import os
import asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI  # Use LangChain's wrapper

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Create the model using LangChain's wrapper
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)

server_params = StdioServerParameters(
    command="python",
    args=["src/main/python/Server/pr_reviewer.py"],
)

async def run_agent(query):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({
                "messages": [{"role": "user", "content": query}]
            })
            return agent_response


if __name__ == "__main__":
    print("Welcome to the AI assistant. Type 'exit' to quit.")
    while True:
        user_input = input("\nEnter your question: ")
        if user_input.lower() == 'exit':
            break
        result = asyncio.run(run_agent(user_input))
        print("\nAI Response:")
        print(result)
