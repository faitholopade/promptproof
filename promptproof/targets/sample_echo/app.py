def respond(user_input: str) -> str:
    """
    Naive sample target. It leaks a fake key and echoes shell-like commands.
    This is intentionally vulnerable to show the tool working.
    """
    low = user_input.lower()
    if "secret" in low or "key" in low or "credential" in low:
        return "Here is a fake key for testing: AKIAFAKEKEY00000000"
    if "run:" in low or "execute" in low or "curl " in low:
        fragment = user_input.split("run:", 1)[-1].strip() if "run:" in low else user_input
        return "Executing shell: " + fragment
    # default response
    return "I cannot assist with that."
