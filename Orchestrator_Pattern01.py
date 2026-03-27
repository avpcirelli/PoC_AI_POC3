import ollama

client = ollama.Client(host='http://localhost:11434')

def call_llm(persona, task_context):
    response = client.chat(model='llama3', messages=[
        {'role': 'system', 'content': persona},
        {'role': 'user', 'content': task_context},
    ])
    return response['message']['content']

# --- SHARED MEMORY ---
state = {
    "topic": "Security risks of using public Wi-Fi for banking",
    "draft": "",
    "critique": "",
    "iterations": 0,
    "max_iterations": 3,
    "approved": False
}

# --- THE REFINEMENT LOOP ---
while not state["approved"] and state["iterations"] < state["max_iterations"]:
    state["iterations"] += 1
    print(f"\n--- Iteration {state['iterations']} ---")

    # STEP 1: RESEARCH/REVISE
    if state["iterations"] == 1:
        prompt = f"Write a detailed report on: {state['topic']}"
    else:
        prompt = f"Rewrite the previous draft: {state['draft']}\n\nBy addressing these critiques: {state['critique']}"
    
    print("Researcher is working...")
    state["draft"] = call_llm("You are a Cyber Security Expert.", prompt)

    # STEP 2: AUDIT
    print("Auditor is evaluating...")
    audit_prompt = f"""
    Review this draft: {state['draft']}
    If the draft is technically accurate and covers at least 3 risks, start your response with 'PASSED'.
    Otherwise, start with 'FAILED' and list the missing points.
    """
    state["critique"] = call_llm("You are a strict Security Auditor.", audit_prompt)

    # STEP 3: THE GATEKEEPER LOGIC
    if state["critique"].strip().upper().startswith("PASSED"):
        state["approved"] = True
        print(">>> Quality Check Passed!")
    else:
        print(">>> Quality Check Failed. Sending back for revision.")

print("\n--- FINAL POLISHED OUTPUT ---")
print(state["draft"])