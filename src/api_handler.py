from typing import Any, Dict, Optional
from typing import List

import requests


def fetch_data_from_api(api_url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Делает HTTP-запрос к API и возвращает данные в виде словаря, если запрос успешен.

    Аргументы:
        api_url (str): URL конечной точки API.
        params (Optional[Dict[str, Any]], optional): Параметры запроса.

    Возвращает:
        Dict[str, Any]: Данные, полученные из API.

    Исключения:
        Exception: Если HTTP-запрос возвращает статус-код, отличный от 200, возникает исключение.
    """
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        if isinstance(response_data, dict):
            return response_data  # Возвращаем только если это словарь
        else:
            raise ValueError("Ожидался ответ типа словаря")
    else:
        raise Exception(f"Ошибка при запросе к API: {response.status_code}")


def extract_items(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Извлекает список элементов из данных API, если ключ 'items' существует.

    Аргументы:
        data (Dict[str, Any]): Данные, полученные из API.

    Возвращает:
        List[Dict[str, Any]]: Список элементов или пустой список.
    """
    if isinstance(data, dict) and "items" in data:
        items = data["items"]
        if isinstance(items, list) and all(isinstance(i, dict) for i in items):
            return items
    return []


def fetch_companies(api_url: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Получает список компаний с указанного URL API.

    Аргументы:
        api_url (str): URL конечной точки API для получения списка компаний.
        params (Optional[Dict[str, Any]], optional): Параметры запроса.

    Возвращает:
        List[Dict[str, Any]]: Список компаний.
    """
    response_data = fetch_data_from_api(api_url, params)
    return extract_items(response_data)


def fetch_vacancies(company_id: int, api_url: str) -> List[Dict[str, Any]]:
    """
    Получает список вакансий для указанной компании по API.

    Аргументы:
        company_id (int): ID компании для получения вакансий.
        api_url (str): URL конечной точки API для получения списка вакансий.

    Возвращает:
        List[Dict[str, Any]]: Список вакансий.
    """
    response_data = fetch_data_from_api(f"{api_url}?employer_id={company_id}")
    return extract_items(response_data)
