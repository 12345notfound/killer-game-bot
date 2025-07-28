class IdError(Exception):
    """Некорректный id"""

    def __init__(self, message):
        super().__init__(message)


class PlayerError(Exception):
    """Некорректные данные игрока(игроков)"""

    def __init__(self, message):
        super().__init__(message)


class ImpossibleRequestError(Exception):
    """Невозможный запрос"""

    def __init__(self, message):
        super().__init__(message)
