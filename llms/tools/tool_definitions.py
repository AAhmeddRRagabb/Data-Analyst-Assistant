# -------------------------------
# LLM Tool Definitions
# -------------------------------

# transcribe
transcribe_function = {
    "type": "function",
    "function": {
        "name": "transcribe",
        "description": "Transcribe the voice recording sent by the user & return the text.",
        "parameters": {
            "type": "object",
            "properties": {
                "audio_path": {
                    "type": "string",
                    "description": "Path of the audio file to transcribe.",
                },
            },
            "required": ["audio_path"],
            "additionalProperties": False,
        },
    },
}


# execute sql query
execute_sql_function = {
    "type": "function",
    "function": {
        "name": "execute_sql_query",
        "description": "Execute the given SQL query & returns the output.",
        "parameters": {
            "type": "object",
            "properties": {
                "sql_query": {
                    "type": "string",
                    "description": "The SQL query to execute.",
                },
            },
            "required": ["sql_query"],
            "additionalProperties": False,
        },
    },
}

# plot graph
plot_graph_tool = {
    "type": "function",
    "function": {
        "name": "plot_graph",
        "description": (
            "Create one plot. If multiple plots are useful, call this function "
            "once per plot and set current_graph_index to 0, 1, 2, and so on.\n"
            "Plots can be one of (bar, line, pie, scatter, or histogram)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "graph_type": {
                    "type": "string",
                    "description": "Type of plot to create, such as line, bar, or scatter.",
                },
                "x": {
                    "type": "array",
                    "items": {},
                    "description": "X-axis values or category labels.",
                },
                "y": {
                    "type": ["array", "null"],
                    "items": {},
                    "description": "Y-axis values, or null when not needed.",
                },
                "title": {"type": "string"},
                "x_label": {"type": "string"},
                "y_label": {"type": "string"},
                "current_graph_index": {
                    "type": "integer",
                    "description": "Zero-based position of this plot among the plots being created. Use 0 for a single plot.",
                },
            },
            "required": ["graph_type", "x"],
            "additionalProperties": False,
        },
    },
}




def get_llm_tool_definitions() -> list[dict]:
    return [
        transcribe_function,
        execute_sql_function,
        plot_graph_tool
    ]