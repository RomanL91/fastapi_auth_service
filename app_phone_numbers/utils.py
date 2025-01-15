def normalize_phone(phone: str) -> str:
    # Удалим лишние символы вроде пробелов, тире, скобок
    stripped = "".join(ch for ch in phone if ch.isdigit() or ch == "+")

    # Если начинается с "+7", оставляем как есть
    if stripped.startswith("+7") and len(stripped) == 12:
        return stripped  # уже +7XXXXXXXXXX

    # Если начинается с "8" и длина 11 — заменяем на +7
    if stripped.startswith("8") and len(stripped) == 11:
        return "+7" + stripped[1:]

    return stripped
