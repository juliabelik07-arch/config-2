
import argparse

from .config import parse_args, print_config


def main(argv=None):

    # Получаем номер этапа
    stage_parser = argparse.ArgumentParser(add_help=False)

    stage_parser.add_argument(
        "--stage",
        type=int,
        choices=[1],
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

    except SystemExit:
        raise

    except Exception as error:
        print(f"\nОшибка выполнения программы: {error}")


if __name__ == "__main__":
    main()
