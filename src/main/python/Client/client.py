import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import uvicorn

load_dotenv()

app = FastAPI()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY,
)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
server_script_path = os.path.join(project_root, "src", "main", "python", "Server", "pr_reviewer.py")

server_params = StdioServerParameters(
    command="python",
    args=[server_script_path],
)

class AskRequest(BaseModel):
    question: str

def convert_to_dict(obj):
    if hasattr(obj, "__dict__"):
        return dict(obj)
    elif isinstance(obj, dict):
        return {key: convert_to_dict(val) for key, val in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_dict(item) for item in obj]
    else:
        return obj

@app.post("/review")
async def ask_question(req: AskRequest):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({
                "messages": [{"role": "user", "content": req.question}]
            })
            result_dict = convert_to_dict(agent_response)
            return {"response": result_dict['messages'][-1]}

# For dev run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
