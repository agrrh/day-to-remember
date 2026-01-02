def text_to_seconds(text: str, has_attachment: bool = False) -> int:
    words = text.split()
    words = filter(None, words)

    # Real world reading speed is about 3 words per second
    base = len(list(words)) / 3

    # Add few moments to take a look at image, if attached
    extra = 5 * int(has_attachment)

    return base + extra
