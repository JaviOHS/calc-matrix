def format_title(title_text):
    """
    Formatea el título reemplazando el texto entre llaves con formato HTML de color.
    Si no hay llaves, resalta la última palabra en naranja.
    """
    if "{" in title_text and "}" in title_text:
        parts = title_text.split("{")
        before_brace = parts[0]
        after_brace = parts[1].split("}")
        highlighted_text = after_brace[0]
        end_text = after_brace[1] if len(after_brace) > 1 else ""
        return f"{before_brace}<span style='color:#ff8103;'>{highlighted_text}</span>{end_text}"
    else:
        return highlight_last_word(title_text)

def highlight_last_word(text):
    """Resalta la última palabra de un texto en color naranja."""
    words = text.split()
    if len(words) >= 1:
        main_text = " ".join(words[:-1])  # Todas las palabras excepto la última
        highlighted_word = f"<span style='color:#ff8103;'>{words[-1]}</span>"  # Última palabra en naranja
        return f"{main_text} {highlighted_word}" if main_text else highlighted_word
    return text