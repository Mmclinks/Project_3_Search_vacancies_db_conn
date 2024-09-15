from typing import Any, Dict, List, Optional

import requests


def fetch_companies(
    api_url: str, params: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Получить список компаний по указанному URL API.

    Аргументы:
        api_url (str): URL конечной точки API для получения списка компаний.
        params (Optional[Dict[str, Any]], optional): Опциональный словарь параметров запроса для включения в запрос.

    Возвращает:
        List[Dict[str, Any]]: Список компаний, полученных из API.
        Если ключ 'items' не найден, возвращает пустой список.

    Исключения:
        Exception: Если HTTP-запрос возвращает статус-код, отличный от 200, возникает исключение.
    """
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        raise Exception(f"Ошибка при получении компаний: {response.status_code}")


def fetch_vacancies(company_id: int, api_url: str) -> List[Dict[str, Any]]:
    """
    Получить список вакансий для конкретной компании по URL API.

    Аргументы:
        company_id (int): ID компании для получения вакансий.
        api_url (str): URL конечной точки API для получения списка вакансий.

    Возвращает:
        List[Dict[str, Any]]: Список вакансий для указанной компании.
         Если ключ 'items' не найден, возвращает пустой список.

    Исключения:
        Exception: Если HTTP-запрос возвращает статус-код, отличный от 200, возникает исключение.
    """
    response = requests.get(f"{api_url}?employer_id={company_id}")
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        raise Exception(f"Ошибка при получении вакансий: {response.status_code}")
