import ollama

client = ollama.Client(host='http://localhost:11434')

def run_agent(role, goal, task_input):
    """This function is our 'Agent Factory'"""
    system_prompt = f"You are a {role}. Your goal is {goal}. Be concise."
    
    response = client.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': task_input},
    ])
    return response['message']['content']

# --- THE PROCESS ---

# 1. Agent A: The Researcher
print("Agent 1 is working...")
research = run_agent(
    role="Tech Scout", 
    goal="Find 3 benefits of using AI agents for small businesses.",
    task_input="Researching AI Agent benefits..."
)

# 2. Agent B: The Critic (Handoff!)
print("Agent 2 is analyzing...")
final_report = run_agent(
    role="Critical Editor",
    goal="Take the research and turn it into a professional LinkedIn post.",
    task_input=f"Here is the research: {research}"
)

print("\n--- FINAL RESULT ---")
print(final_report)