
# ЭТАП 2. Сбор данных
# Файл отвечает за получение информации о npm-пакетах
# и извлечение их прямых зависимостей.

import json
import urllib.request
import urllib.error

from urllib.parse import quote, urlparse, unquote


# 1. Получение JSON-данных по URL
def get_json(url):

    # Создаём HTTP-запрос к серверу
    request = urllib.request.Request(
        url,
        headers={
            # Указываем название нашей программы
            "User-Agent": "DependencyGraph/1.0",

            # Сообщаем серверу, что ожидаем JSON
            "Accept": "application/json"
        }
    )

    try:

        # Отправляем запрос и ожидаем ответ не более 15 секунд
        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            # Читаем ответ сервера и декодируем его в UTF-8
            data = response.read().decode("utf-8")

            # Преобразуем JSON-текст в словарь Python
            return json.loads(data)

    except urllib.error.HTTPError as error:

        # Обрабатываем HTTP-ошибки, например пакет не найден
        raise RuntimeError(
            f"Ошибка HTTP: {error.code}"
        )

    except urllib.error.URLError as error:

        # Обрабатываем ошибки подключения к серверу
        raise RuntimeError(
            f"Ошибка подключения: {error.reason}"
        )

    except json.JSONDecodeError:

        # Обрабатываем неправильный формат JSON
        raise RuntimeError(
            "Получены некорректные JSON-данные"
        )


# 2. Получение информации о заданном npm-пакете
def get_package_info(package_name, repository_url):

    # Разбираем адрес Registry на отдельные части
    parsed = urlparse(repository_url)

    # Кодируем имя пакета для использования в URL
    # Это необходимо, например, для пакетов с символом @
    encoded_name = quote(package_name, safe="@")

    # Получаем путь из URL и декодируем его
    package_path = unquote(parsed.path).strip("/")

    # Проверяем, передан ли полный URL конкретного пакета
    if package_path.endswith("/latest"):

        # Убираем окончание /latest
        url_package_name = package_path[:-len("/latest")]

        # Проверяем, совпадает ли пакет в URL с заданным именем
        if url_package_name == package_name:

            # Используем полный URL, переданный пользователем
            url = repository_url

        else:

            raise RuntimeError(
                "URL не соответствует указанному имени пакета."
            )

    else:

        # Если передан только адрес Registry,
        # самостоятельно формируем URL нужного пакета
        url = (
            f"{repository_url.rstrip('/')}/"
            f"{encoded_name}/latest"
        )

    # Получаем JSON по сформированному URL
    return get_json(url)


# 3. Извлечение прямых зависимостей из JSON
def get_direct_dependencies(package_info):

    # Проверяем, что полученные данные являются словарём
    if not isinstance(package_info, dict):
        raise RuntimeError(
            "Неверный формат JSON."
        )

    # Получаем поле dependencies
    # Если такого поля нет, возвращаем пустой словарь
    dependencies = package_info.get(
        "dependencies",
        {}
    )

    # Проверяем, что dependencies является словарём
    if not isinstance(dependencies, dict):
        raise RuntimeError(
            "Поле dependencies должно быть объектом."
        )

    # Возвращаем названия зависимостей и их версии
    return dependencies


# 4. Получение прямых зависимостей заданного пакета
def fetch_package_dependencies(package_name, repository_url):

    # Получаем полную информацию о пакете из npm Registry
    package_info = get_package_info(
        package_name,
        repository_url
    )

    # Извлекаем из JSON прямые зависимости
    dependencies = get_direct_dependencies(
        package_info
    )

    # Возвращаем найденные зависимости
    return dependencies
