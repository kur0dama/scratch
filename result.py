from typing import Any
from abc import abstractmethod


def wrap_result(func):
    def wrapper(*args, **kwargs):
        try:
            return Ok(value=func(*args, **kwargs))
        except Exception as e:
            return Err(error_cls=e.__class__.__name__, error_msg=e)

    return wrapper


class Result:
    def __init__(self):
        pass

    def is_ok(self) -> bool:
        return isinstance(self, Ok)

    def is_err(self) -> bool:
        return isinstance(self, Err)

    @abstractmethod
    def unwrap(self):
        ...


class Ok(Result):
    def __init__(self, value: Any):
        super().__init__()
        self._value = value

    def __repr__(self) -> str:
        return f"<Result: {self.__class__.__name__}, value={str(self._value)}>"

    def __bool__(self) -> bool:
        return True

    def unwrap(self) -> None:
        return self._value


class Err(Result):
    def __init__(self, error_cls: str, error_msg: str):
        super().__init__()
        self._error_cls = error_cls
        self._error_msg = error_msg

    def __repr__(self) -> str:
        return f"<Result: {self.__class__.__name__}, error_cls='{self._error_cls}', error_msg='{self._error_msg}'>"

    def __bool__(self) -> bool:
        return False

    def unwrap(self) -> None:
        pass


@wrap_result
def divide_1_by(n) -> Result:
    return 1 / n


for i in [1, 0]:
    result = divide_1_by(i)
    print(result)
    print(result.is_ok())
    if result:
        print(result.unwrap())
