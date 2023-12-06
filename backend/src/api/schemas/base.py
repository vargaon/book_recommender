from typing import Any


class BaseQueryParameters:
    """Class to represent base query parameters"""

    def dict(self) -> dict[str, Any]:
        """Get dictionary of query parameters

        :return: Query parameters dictionary
        :rtype: dict[str, Any]
        """

        return self.__dict__
