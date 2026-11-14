
import argparse

# Импортируем настройки программы
from .config import parse_args, print_config

# Импортируем получение зависимостей из npm Registry
from .fetcher import fetch_package_dependencies

# Импортируем построение графа зависимостей
from .graph import build_graph

from .visualizer import visualize_graph

from .dependency_order import calculate_loading_order


def main(argv=None):

    # Создаём обработчик номера этапа
    stage_parser = argparse.ArgumentParser(add_help=False)

    # Разрешаем запускать первые три этапа
    stage_parser.add_argument(
        "--stage",
        type=int,
        choices=[1, 2, 3, 4],
        default=1,
        help="Номер этапа практической работы"
    )

    # Отделяем номер этапа от остальных параметров
    stage_args, remaining_args = stage_parser.parse_known_args(argv)

    try:

        # Получаем настройки программы
        config = parse_args(remaining_args)

        # Выводим настройки на экран
        print_config(config)

        # ЭТАП 1. Настройка конфигурации
        if stage_args.stage == 1:

            print("\nЭтап 1. Настройка конфигурации")
            print("--------------------------------")

            print("Конфигурация успешно загружена.")
            print("Все параметры прошли проверку.")

        # ЭТАП 2. Сбор данных
        elif stage_args.stage == 2:

            print("\nЭтап 2. Сбор данных")
            print("--------------------------------")

            # Получаем прямые зависимости пакета
            dependencies = fetch_package_dependencies(
                config.package,
                config.repository
            )

            # Выводим название анализируемого пакета
            print(
                f"\nПрямые зависимости пакета {config.package}:"
            )

            # Проверяем, есть ли зависимости
            if dependencies:

                # Перебираем зависимости и их версии
                for number, (name, version) in enumerate(
                    dependencies.items(),
                    start=1
                ):

                    print(f"{number}. {name} — {version}")

            else:

                print("У пакета нет прямых зависимостей.")

        # ЭТАП 3. Построение графа зависимостей
        elif stage_args.stage == 3:

            print("\nЭтап 3. Построение графа зависимостей")
            print("--------------------------------")

            # Строим граф с учётом максимальной глубины
            graph, cycles = build_graph(config)

            # Выводим все вершины и их зависимости
            print("\nПостроенный граф:")

            for package, dependencies in graph.items():

                print(f"{package} -> {dependencies}")

            # Проверяем, найдены ли циклы
            if cycles:

                print("\nОбнаружены циклические зависимости:")

                # Выводим найденные циклические связи
                for source, target in sorted(cycles):

                    print(f"{source} -> {target}")

            else:

                print("\nЦиклические зависимости не обнаружены.")

            # Создаём изображение графа
            visualize_graph(
            graph,
            cycles,
            config.output
            )

            print("\nПостроение графа завершено.")

        
        # ЭТАП 4. Определение порядка загрузки
        elif stage_args.stage == 4:

            print("\nЭтап 4. Дополнительные операции")
            print("--------------------------------")

            # Строим граф зависимостей
            graph, cycles = build_graph(config)

            # Показываем построенный граф
            print("\nПостроенный граф:")

            for package, dependencies in graph.items():

                print(f"{package} -> {dependencies}")

            # Вычисляем порядок загрузки пакетов
            loading_order, unresolved = calculate_loading_order(graph)

            print("\nПорядок загрузки пакетов:")

            # Если остались необработанные пакеты,
            # полный порядок загрузки определить нельзя
            if unresolved:

                print(
                    "Невозможно определить полный порядок загрузки."
                )

                # Показываем циклические зависимости
                if cycles:

                    print("\nОбнаруженные циклические зависимости:")

                    for source, target in sorted(cycles):

                        print(f"{source} -> {target}")

                # Выводим пакеты, которые остались необработанными
                print("\nНеобработанные пакеты:")

                for package in unresolved:

                    print(package)

                # Показываем ту часть порядка,
                # которую удалось определить
                if loading_order:

                    print("\nПакеты с определённым порядком загрузки:")

                    for number, package in enumerate(
                        loading_order,
                        start=1
                    ):

                        print(f"{number}. {package}")

            # Если граф пустой
            elif not loading_order:

                print("Нет пакетов для загрузки.")

            # Если циклов нет и порядок определён
            else:

                for number, package in enumerate(
                    loading_order,
                    start=1
                ):

                    print(f"{number}. {package}")

            print("\nОпределение порядка загрузки завершено.")


    except SystemExit:
        # Не изменяем стандартную обработку argparse
        raise

    except Exception as error:
        # Выводим информацию об ошибке
        print(f"\nОшибка выполнения программы: {error}")


# Запускаем программу
if __name__ == "__main__":
    main()
