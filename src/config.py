# 1 этап
#настройка программы


import argparse
from dataclasses import dataclass
from pathlib import Path


# Класс для хранения всех параметров программы
@dataclass
class Config:
    package: str #название пакета
    repository: str  #адрес репозитория или путь к тестовому JSON
    test_mode: bool  #включён ли тестовый режим
    test_file: str  
    output: str  #имя выходного файла
    max_depth: int  #максимальная глубина обхода


# Функция получения параметров командной строки
def parse_args(args=None):

    parser = argparse.ArgumentParser( # отвечает за обработку параметров
        description="Построение графа зависимостей npm-пакетов."
    )

    # Имя анализируемого пакета
    parser.add_argument(
        "--package",
        required=True,
        help="Имя анализируемого npm-пакета."
    )

    # URL репозитория
    parser.add_argument(
        "--repository",
        default="https://github.com/",
        help="URL GitHub-репозитория."
    )

    # Режим тестирования
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Включить тестовый режим."
    )

    # Путь к тестовому файлу
    parser.add_argument(
        "--test-file",
        default="test_data/repository.json",
        help="Путь к файлу с тестовым графом."
    )

    # Имя выходного файла
    parser.add_argument(
        "--output",
        default="dependencies.svg",
        help="Имя файла с изображением графа."
    )

    # Максимальная глубина анализа
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Максимальная глубина анализа."
    )

    # Получаем переданные пользователем параметры
    namespace = parser.parse_args(args)

    # Проверяем имя пакета
    if not namespace.package.strip():
        parser.error("Имя пакета не может быть пустым.")

    # Проверяем глубину
    if namespace.max_depth < 0:
        parser.error(
            "Максимальная глубина не может быть отрицательной."
        )

    # Проверяем формат выходного файла
    if not namespace.output.lower().endswith(".svg"):
        parser.error(
            "Выходной файл должен иметь расширение .svg."
        )

    # Проверяем наличие тестового файла
    if namespace.test_mode and not Path(
        namespace.test_file
    ).is_file():
        parser.error(
            f"Тестовый файл не найден: {namespace.test_file}"
        )

    # Проверяем URL репозитория
    if not namespace.test_mode and not namespace.repository.startswith(
        ("http://", "https://")
    ):
        parser.error(
            "URL репозитория должен начинаться с http:// или https://."
        )

    # Возвращаем настройки в виде объекта Config
    return Config(
        package=namespace.package.strip(),
        repository=namespace.repository,
        test_mode=namespace.test_mode,
        test_file=namespace.test_file,
        output=namespace.output,
        max_depth=namespace.max_depth
    )


# Функция вывода настроек в формате ключ-значение
def print_config(config):

    print("Параметры запуска:")

    print(f"package = {config.package}")
    print(f"repository = {config.repository}")
    print(f"test_mode = {config.test_mode}")
    print(f"test_file = {config.test_file}")
    print(f"output = {config.output}")
    print(f"max_depth = {config.max_depth}")

    #python -m src.main --stage 1 --package axios
    #python -m src.main --stage 1 --package axios --max-depth -1