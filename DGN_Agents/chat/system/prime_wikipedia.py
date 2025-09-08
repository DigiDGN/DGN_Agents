# Optional wiki priming provider

def prime(character_or_cmd: str) -> str:
    from DGN_Agents.utils import wikipedia_search_lookup
    return wikipedia_search_lookup(character_or_cmd)
