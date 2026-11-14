
import argparse

from .config import parse_args, print_config
from .fetcher import fetch_package_dependencies
from .graph import build_graph

def main(argv=None):

    # Получаем номер этапа
    stage_parser = argparse.ArgumentParser(add_help=False)

    stage_parser.add_argument(
        "--stage",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Номер этапа практической работы"
    )

    # Отделяем номер этапа от остальных параметров
    stage_args, remaining_args = stage_parser.parse_known_args(argv)

    try:

        # Получаем и проверяем конфигурацию
        config = parse_args(remaining_args)

        # Выводим параметры запуска
        print_config(config)

        # ЭТАП 1. Конфигурация
        if stage_args.stage == 1:

            print("\nЭтап 1. Настройка конфигурации")
            print("--------------------------------")

            print("Конфигурация успешно загружена.")
            print("Все параметры прошли проверку.")

        # ЭТАП 2. Сбор данных
        elif stage_args.stage == 2:

            print("\nЭтап 2. Сбор данных")
            print("--------------------------------")

            # Получаем прямые зависимости заданного пакета
            dependencies = fetch_package_dependencies(
                config.package,
                config.repository
            )

            # Выводим название анализируемого пакета
            print(
                f"\nПрямые зависимости пакета "
                f"{config.package}:"
            )

            # Проверяем, есть ли у пакета зависимости
            if dependencies:

                # Перебираем все зависимости из словаря
                for number, (name, version) in enumerate(
                    dependencies.items(),
                    start=1
                ):

                    # Выводим номер, название и версию зависимости
                    print(
                        f"{number}. {name} — {version}"
                    )

            else:

                # Если зависимостей нет, выводим сообщение
                print("У пакета нет прямых зависимостей")
           
        
        # ЭТАП 3. Построение графа зависимостей
        elif stage_args.stage == 3:

            print("\nЭтап 3. Построение графа зависимостей")
            print("--------------------------------")

            # Строим граф с учётом максимальной глубины
            graph, cycles = build_graph(config)

            # Выводим полученный граф
            print("\nПостроенный граф:")

            for package, dependencies in graph.items():

                print(
                    f"{package} -> {dependencies}"
                )

            # Проверяем наличие циклических зависимостей
            if cycles:

                print("\nОбнаружены циклические зависимости:")

                # Выводим каждое циклическое ребро
                for source, target in sorted(cycles):

                    print(
                        f"{source} -> {target}"
                    )

            else:

                print(
                    "\nЦиклические зависимости не обнаружены"
                )

            print("\nПостроение графа завершено")

    except SystemExit:
        # Сохраняем стандартную обработку ошибок argparse
        raise

    except Exception as error:
        # Выводим сообщение, если возникла ошибка
        print(f"\nОшибка выполнения программы: {error}")


if __name__ == "__main__":
    main()

