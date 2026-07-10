# Linode Autogen Quick Deploy App

AutoGen is Microsoft's open-source framework for building AI agents that collaborate with one another. Instead of creating a single chatbot, AutoGen allows you to create multiple specialized AI agents that communicate, delegate work, review each other's output, execute code, and interact with external systems.

| Software  | Version   | Description               |
| :---      | :----     | :---                      |
| Autogen   | `latest`  | Autogen binary client     |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Deployment Details

Once the deployment has finished running you will be able to create a project and start using Autogen. To start, you can use Autogen weather example but modify it slightly to work this vLLM. This is an example using a fake weather tool.

1. Create a working directory called weather.

```bash
mkdir weather
```

2. Create a file called `weather.py` with the following content:

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


model_client = OpenAIChatCompletionClient(
    model="Qwen/Qwen3-14B-AWQ",
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "qwen",
    },
)


async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is 73 degrees and Sunny."


agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="You are a helpful assistant.",
    reflect_on_tool_use=True,
    model_client_stream=True,
)


async def main():
    await Console(
        agent.run_stream(
            task="What is the weather in New York?"
        )
    )

    await model_client.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### What's Next?

The strenght of Autogen can be harvested by creating a team of agents that accomplish a particular task. To understand how you can create, observe and control a team of agents.

- https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/teams.html

## Resources

- [Quick Start](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/quickstart.html)
- [Installation](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/quickstart.html)
- [Models](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/models.html)