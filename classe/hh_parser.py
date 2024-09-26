import requests
from typing import Any


class HHParser:
    def __init__(self) -> None:
        self.__url = None
        self.__params = None

    def __get_request(self) -> Any:
        response = requests.get(self.__url, self.__params)
        if response.status_code == 200:
            return response.json()["items"]
        return ""

    def get_employers(self) -> Any:
        self.__url = "https://api.hh.ru/employers"
        self.__params = {
            "sort_by": "by_vacancies_open",
            "per_page": 10
        }
        return self.__get_request()

    def get_vacancies(self, employer_id: int) -> Any:
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {
            "employer_id": employer_id,
            "per_page": 50
        }
        return self.__get_request()
