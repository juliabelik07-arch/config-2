# ЭТАП 3. Построение графа зависимостей
# Обход выполняется алгоритмом DFS без рекурсии.

from .fetcher import (
    fetch_package_dependencies,
    load_test_repository
)


# 1. Построение графа зависимостей
def build_graph(config):

    # Если включён тестовый режим,
    # загружаем зависимости из локального JSON-файла
    if config.test_mode:
        repository = load_test_repository(config.test_file)

        # Функция получения зависимостей из тестового графа
        def get_dependencies(package):
            return repository.get(package, [])

    else:

        # Функция получения зависимостей из npm Registry
        def get_dependencies(package):
            dependencies = fetch_package_dependencies(
                package,
                config.repository
            )

            # Возвращаем только названия пакетов
            return list(dependencies.keys())

    # Создаём пустой граф
    graph = {}

    # Множество уже обработанных пакетов
    visited = set()

    # Стек для нерекурсивного DFS
    # В стеке хранятся название пакета и его глубина
    stack = [(config.package, 0)]

    # Пока в стеке есть пакеты
    while stack:

        # Забираем последний добавленный пакет
        package, depth = stack.pop()

        # Если пакет уже обрабатывался, пропускаем его
        if package in visited:
            continue

        # Отмечаем пакет как обработанный
        visited.add(package)

        # Добавляем пакет в граф
        graph[package] = []

        # Если достигли максимальной глубины,
        # дальше зависимости этого пакета не загружаем
        if depth >= config.max_depth:
            continue

        # Получаем прямые зависимости текущего пакета
        dependencies = get_dependencies(package)

        # Убираем повторяющиеся зависимости,
        # сохраняя первоначальный порядок
        dependencies = list(dict.fromkeys(dependencies))

        # Записываем зависимости в граф
        graph[package] = dependencies

        # Добавляем зависимости в стек
        # Обратный порядок нужен для сохранения порядка обхода
        for dependency in reversed(dependencies):

            if dependency not in visited:
                stack.append((dependency, depth + 1))

    # Добавляем в граф найденные пакеты,
    # у которых ещё нет собственного списка зависимостей
    for dependencies in list(graph.values()):
        for dependency in dependencies:
            if dependency not in graph:
                graph[dependency] = []

    # Ищем циклические зависимости
    cycles = find_cycles(graph)

    # Возвращаем граф и найденные циклы
    return graph, cycles


# 2. Поиск циклических зависимостей
def find_cycles(graph):

    # 0 — пакет ещё не посещён
    # 1 — пакет сейчас находится в процессе обхода
    # 2 — пакет полностью обработан
    color = {package: 0 for package in graph}

    # Список найденных циклических рёбер
    cycles = set()

    # Проверяем все вершины графа
    for start in graph:

        # Если пакет уже обработан, пропускаем его
        if color[start] != 0:
            continue

        # Помечаем начальный пакет как посещаемый
        color[start] = 1

        # Стек хранит пакет и итератор его зависимостей
        stack = [
            (start, iter(graph.get(start, [])))
        ]

        # Выполняем обход без рекурсии
        while stack:

            # Получаем текущий пакет и его итератор
            package, dependencies = stack[-1]

            try:

                # Берём следующую зависимость
                dependency = next(dependencies)

                # Если зависимость находится в процессе обхода,
                # значит обнаружен цикл
                if color.get(dependency, 0) == 1:

                    cycles.add((package, dependency))

                # Если зависимость ещё не посещалась,
                # переходим к её зависимостям
                elif color.get(dependency, 0) == 0:

                    color[dependency] = 1

                    stack.append(
                        (
                            dependency,
                            iter(graph.get(dependency, []))
                        )
                    )

            except StopIteration:

                # Если зависимости закончились,
                # завершаем обработку текущего пакета
                color[package] = 2

                # Удаляем пакет из стека
                stack.pop()

    # Возвращаем найденные циклические рёбра
    return cycles
