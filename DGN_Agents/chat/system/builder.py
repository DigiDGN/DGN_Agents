# Builds system prompt

def build_system_prompt(system=None, character=None, character_command=None, prime=False):
    prompt = system or "You are a helpful assistant."
    if prime and (character or character_command):
        try:
            from .prime_wikipedia import prime as wiki_prime
            prime_text = wiki_prime(character or character_command)
            prompt = f"{prompt}\n{prime_text}"
        except Exception:
            pass
    return prompt
