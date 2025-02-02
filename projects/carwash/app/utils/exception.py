from fastapi import HTTPException, status


class ObjectNotFoundException(HTTPException):
    def __init__(self, model_name: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model_name} not found")


class InvalidCredentialsException(HTTPException):
    def __init__(self, detail: str = "Invalid username or password"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)