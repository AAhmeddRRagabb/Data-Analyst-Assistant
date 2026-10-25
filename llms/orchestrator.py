from pathlib import Path
from .context import get_system_prompt
from helpers.system_settings import get_system_settings

from openai import OpenAI
from .tools import handle_tool_calls
from .tools import get_llm_tool_definitions

def run_orchestrator(
    user_prompt: str | None = None, 
    voice_path: str | Path | None = None,
    tools: list = get_llm_tool_definitions()
) -> str:
    system_settings = get_system_settings()

    if user_prompt is None and voice_path is None:
        raise ValueError("No Input Given")

    if voice_path is not None:
        user_message = f"The user sent a voice recording.\nAudio file path: {Path(voice_path).as_posix()}"
    else:
        user_message = user_prompt

    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    with OpenAI(
        api_key=system_settings.GROQ_API_KEY,
        base_url=system_settings.GROQ_BASE_URL,
    ) as client:
        for _ in range(system_settings.ORCHESTRATOR_MAX_STEPS):
            response = client.chat.completions.create(
                model=system_settings.TEXT_TO_TEXT_LLM,
                messages=messages,
                tools=tools,
            )
            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            messages.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in message.tool_calls
                ],
            })
            messages.extend(handle_tool_calls(message))

    raise RuntimeError(f"Supervisor did not finish within {system_settings.ORCHESTRATOR_MAX_STEPS} steps.")
