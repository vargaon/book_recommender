from typing import Any

from fastapi import HTTPException, status


class HTTPBadRequestError(HTTPException):
    """Class to represent http_bad_request exception with status code 400"""

    def __init__(
        self, name: str, value: Any, detail: str, headers: dict[str, Any] | None = None
    ) -> None:
        """Construct method

        :param name: Name of invalid argument
        :type name: str
        :param value: Value of invalid argument
        :type value: Any
        :param detail: Detail of exception
        :type detail: str
        :param headers: Response headers, defaults to None
        :type headers: dict[str, Any] | None, optional
        """

        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)

        self.name = name
        self.value = str(value)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, name={self.name!r}, value={self.value!r}, detail={self.detail!r})"


class HTTPNotFoundError(HTTPException):
    """Class to represent http_not_found exception with status code 404"""

    def __init__(self, detail: str, headers: dict[str, Any] | None = None) -> None:
        """Construct method

        :param detail: Detail of exception
        :type detail: str
        :param headers: Response headers, defaults to None
        :type headers: dict[str, Any] | None, optional
        """

        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)


class HTTPUnauthorizedError(HTTPException):
    """Class to represent http_unauthorized exception with status code 401"""

    def __init__(self, detail: str, headers: dict[str, Any] | None = None) -> None:
        """Construct method

        :param detail: Detail of exception
        :type detail: str
        :param headers: Response headers, defaults to None
        :type headers: dict[str, Any] | None, optional
        """

        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)


class HTTPUnprocessableEntityError(HTTPException):
    """Class to represent http_unprocessable_entity exception with status code 422"""

    def __init__(self, detail: str, headers: dict[str, Any] | None = None) -> None:
        """Construct method

        :param detail: Detail of exception
        :type detail: str
        :param headers: Response headers, defaults to None
        :type headers: dict[str, Any] | None, optional
        """

        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, headers)


class HTTPConflictError(HTTPException):
    """Class to represent http_conflict exception with status code 409"""

    def __init__(self, detail: str, headers: dict[str, Any] | None = None) -> None:
        """Construct method

        :param detail: Detail of exception
        :type detail: str
        :param headers: Response headers, defaults to None
        :type headers: dict[str, Any] | None, optional
        """

        super().__init__(status.HTTP_409_CONFLICT, detail, headers)
