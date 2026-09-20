"""Вспомогательные функции безопасного ввода."""


def input_non_empty(prompt: str) -> str:
    """Получить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значение не может быть пустым.")


def input_int(
    prompt: str,
    min_value: int | None = None,
    max_value: int | None = None,
) -> int:
    """Получить целое число с проверкой диапазона."""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value is not None and value < min_value:
                raise ValueError
            if max_value is not None and value > max_value:
                raise ValueError
            return value
        except ValueError:
            print("Введите корректное целое число.")


def input_choice(prompt: str, choices: set[str]) -> str:
    """Получить одно значение из набора допустимых вариантов."""
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        print(f"Допустимые варианты: {', '.join(sorted(choices))}.")
