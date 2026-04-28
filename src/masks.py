def mask_card_number(card_str: str) -> str:
    """Маскирует номер карты или счета."""
    if not card_str:
        return "Нет данных"
    if "Счет" in card_str:
        numbers = ''.join(filter(str.isdigit, card_str))
        if len(numbers) >= 4:
            return f"Счет **{numbers[-4:]}"
        return card_str
    parts = card_str.split()
    if len(parts) >= 2:
        card_num = parts[-1]
        if len(card_num) >= 16:
            masked = f"{card_num[:4]} {card_num[4:6]}** **** {card_num[-4:]}"
            return f"{parts[0]} {masked}"
    return card_str
