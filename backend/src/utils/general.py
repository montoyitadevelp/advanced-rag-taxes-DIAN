def chunk_text(text: str, max_chars: int = 1500):
    """
    Splits the input text into chunks of a specified maximum number of characters.

    Args:
        text (str): The text to be split into chunks.
        max_chars (int, optional): The maximum number of characters per chunk. Defaults to 1500.

    Returns:
        List[str]: A list of text chunks, each with a length up to max_chars.
    """
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]