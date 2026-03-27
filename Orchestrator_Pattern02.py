import ollama

client = ollama.Client(host='http://localhost:11434')

def call_agent(role_name, persona, user_query):
    print(f"\n[SYSTEM] Routing to Specialist: {role_name}...")
    response = client.chat(model='llama3', messages=[
        {'role': 'system', 'content': persona},
        {'role': 'user', 'content': user_query},
    ])
    return response['message']['content']

# --- THE ROUTER LOGIC ---
def route_request(user_input):
    # The 'Router' is just a fast LLM call to categorize the intent
    router_persona = """
    Analyze the user's request. Categorize it into EXACTLY ONE of these categories: 
    'CODING', 'CREATIVE', or 'GENERAL'. 
    Respond with ONLY the word.
    """
    
    category = client.chat(model='llama3', messages=[
        {'role': 'system', 'content': router_persona},
        {'role': 'user', 'content': user_input},
    ])['message']['content'].strip().upper()

    # --- THE SWITCHBOARD ---
    if "CODING" in category:
        return call_agent("Senior Developer", "You are an expert Python coder. Provide clean code.", user_input)
    
    elif "CREATIVE" in category:
        return call_agent("Marketing Copywriter", "You are a creative writer. Use engaging, emotional language.", user_input)
    
    else:
        return call_agent("General Assistant", "You are a helpful assistant. Give factual, concise answers.", user_input)

# --- TESTING THE ROUTER ---
queries = [
    "Write a Python script to sort a list of numbers",
    "Write a catchy slogan for a new organic coffee brand",
    "What is the capital of Italy?"
]

for q in queries:
    print(f"\nUSER QUERY: {q}")
    result = route_request(q)
    print(f"RESULT: {result}")
    print("-" * 30)