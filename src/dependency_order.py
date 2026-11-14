
# ЭТАП 4. Определение порядка загрузки пакетов

from collections import deque


# Функция определения порядка загрузки зависимостей
def calculate_loading_order(graph):

    # Получаем все пакеты, которые есть в графе
    packages = list(graph.keys())

    # Добавляем пакеты, которые встречаются
    # в списках зависимостей, но отсутствуют среди ключей
    for dependencies in graph.values():

        for dependency in dependencies:

            if dependency not in packages:
                packages.append(dependency)

    # Для каждого пакета храним количество
    # его ещё не загруженных зависимостей
    dependency_count = {}

    # Для каждой зависимости храним пакеты,
    # которые от неё зависят
    dependents = {
        package: []
        for package in packages
    }

    # Заполняем количество зависимостей
    for package in packages:

        # Убираем повторяющиеся зависимости
        dependencies = list(
            dict.fromkeys(graph.get(package, []))
        )

        # Запоминаем количество зависимостей пакета
        dependency_count[package] = len(dependencies)

        # Запоминаем, какие пакеты зависят от текущего
        for dependency in dependencies:

            dependents[dependency].append(package)

    # Создаём очередь пакетов, у которых
    # нет зависимостей
    queue = deque(
        package
        for package in packages
        if dependency_count[package] == 0
    )

    # Сюда записываем итоговый порядок загрузки
    loading_order = []

    # Пока в очереди есть пакеты
    while queue:

        # Извлекаем первый пакет из очереди
        package = queue.popleft()

        # Добавляем его в порядок загрузки
        loading_order.append(package)

        # Находим пакеты, которые зависят от него
        for dependent in dependents[package]:

            # Уменьшаем количество незагруженных зависимостей
            dependency_count[dependent] -= 1

            # Если все зависимости пакета уже обработаны,
            # добавляем его в очередь
            if dependency_count[dependent] == 0:

                queue.append(dependent)

    # Пакеты, которые остались с зависимостями,
    # невозможно включить в полный порядок
    unresolved = [
        package
        for package in packages
        if dependency_count[package] > 0
    ]

    # Возвращаем порядок загрузки и необработанные пакеты
    return loading_order, unresolved

#python -m src.main --stage 4 --package A --test-mode --test-file test_data/repository.json --max-depth 2
#python -m src.main --stage 4 --package A --test-mode --test-file test_data/repository_empty.json --max-depth 2
#python -m src.main --stage 4 --package A --test-mode --test-file test_data/repository_no_cycle.json --max-depth 3
#python -m src.main --stage 4 --package axios --max-depth 2