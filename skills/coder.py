from typing import Dict

from brain.ollama_interface import OllamaInterface


def generate_code(task_description: str) -> Dict[str, str]:
    """
    Uses CodeLlama via Ollama to generate code for the requested task.
    Does not execute code. Returns a dict with 'explanation' and 'code'.
    """
    ollama = OllamaInterface(model="codellama:7b-instruct")
    system_prompt = (
        "You are a careful coding assistant. Generate minimal, correct code and a brief explanation. "
        "Do not include dangerous commands."
    )
    user_prompt = (
        "Task: " + task_description + "\n"
        "Provide a short explanation followed by code in a fenced block."
    )
    resp = ollama.generate(system_prompt, user_prompt, temperature=0.2, max_tokens=1024)

    # Simple parsing: try to split explanation vs code block
    explanation = resp
    code = ""
    if "```" in resp:
        parts = resp.split("```")
        if len(parts) >= 2:
            explanation = parts[0].strip()
            # code language may be in the first line after ```
            code = parts[1]
            if "\n" in code:
                code = code.split("\n", 1)[1]
            code = code.strip()

    return {"explanation": explanation, "code": code}
