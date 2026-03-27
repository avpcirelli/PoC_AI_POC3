import ollama

client = ollama.Client(host='http://localhost:11434')

# --- THE TOOLS (Python Functions) ---
def read_local_file(filename):
    print(f"[TOOL] Reading file: {filename}...")
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: File not found."

# --- THE AGENT LOGIC ---
def tool_using_agent(user_query):
    # We tell the AI it has a 'Tool' available
    system_persona = """
    You are a Research Assistant. You have access to a tool: read_local_file(filename).
    If you need information from a file, respond ONLY with this format:
    ACTION: read_local_file('filename.txt')
    Otherwise, give the final answer.
    """

    # 1. First "Thought"
    response = client.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_persona},
        {'role': 'user', 'content': user_query}
    ])
    
    content = response['message']['content']

    # 2. Check if the Agent wants to use the tool
    if "ACTION: read_local_file" in content:
        # Simple string parsing to get the filename
        filename = content.split("'")[1]
        
        # EXECUTE THE TOOL (Observation)
        file_content = read_local_file(filename)
        
        # 3. Final Answer (Feeding the observation back to the AI)
        final_response = client.chat(model='llama3', messages=[
            {'role': 'system', 'content': system_persona},
            {'role': 'user', 'content': user_query},
            {'role': 'assistant', 'content': content}, # The AI's thought
            {'role': 'user', 'content': f"OBSERVATION: {file_content}"} # The tool result
        ])
        return final_response['message']['content']
    
    return content

# --- TESTING ---
print("QUERY: What is the secret code in knowledge.txt?")
result = tool_using_agent("What is the secret code in C:/tmp/PoC_AI_3/knowledge.txt?")
print(f"FINAL ANSWER: {result}")