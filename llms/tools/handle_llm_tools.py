
import json

from core.database import execute_sql_query
from core.plotting import plot_graph
from core.audio_manipulation import transcribe




tools_dict = {
    'transcribe': transcribe,
    'plot_graph': plot_graph,
    'execute_sql_query': execute_sql_query
}


def handle_tool_calls(message):
    responses = []
    
    for tool_call in message.tool_calls:
        tool_name = tool_call.function.name
        tool_called = tools_dict.get(tool_name, None) 
        if not tool_called:

            responses.append({
                'role': 'tool',
                'tool_call_id': tool_call.id,
                'content': f'Tool: {tool_name} does not exist.'
            })

            continue

        try:
            tool_arguments = json.loads(tool_call.function.arguments)
            result = tool_called(**tool_arguments)
            content = result if isinstance(result, str) else json.dumps(result, default=str)
        except Exception as error:
            content = json.dumps({'success': False, 'tool': tool_name, 'error_type': type(error).__name__, 'error': str(error), 'hint': 'Check the tool schema, correct the arguments, and retry automatically.'})
        
        responses.append({
            "role": "tool",
            "content": content,
            "tool_call_id": tool_call.id
        })
        
    return responses