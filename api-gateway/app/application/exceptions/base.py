class AppError(Exception):
    code: str = "APP_ERROR"
    message: str = "Application error"

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
    ):
        self.message = message or self.message
        self.code = code or self.code

        super().__init__(self.message)
