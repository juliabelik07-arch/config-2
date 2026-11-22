# Этап 5. Визуализация
# Файл отвечает за создание изображения графа в формате SVG.


import math
from pathlib import Path
from xml.sax.saxutils import escape


# Функция построения и сохранения графа
def visualize_graph(graph, cycles, output):

    # Проверяем, что граф не пустой
    if not graph:
        raise RuntimeError("Граф пустой")

    # Получаем список всех пакетов
    packages = list(graph.keys())

    # Добавляем пакеты, которые встречаются только в зависимостях
    for dependencies in graph.values():
        for dependency in dependencies:
            if dependency not in packages:
                packages.append(dependency)

    # Создаём идентификаторы для вершин Mermaid
    node_ids = {
        package: f"node{i}"
        for i, package in enumerate(packages)
    }

    # Создаём путь к выходному SVG-файлу
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Создаём имя файла Mermaid
    mermaid_path = output_path.with_suffix(".mmd")

    # ------------------------------------------------
    # ЧАСТЬ 1. СОЗДАНИЕ ТЕКСТОВОГО ПРЕДСТАВЛЕНИЯ MERMAID
    # ------------------------------------------------

    # Начинаем описание направленного графа
    mermaid = ["flowchart TD"]

    # Добавляем вершины графа
    for package in packages:

        node_id = node_ids[package]

        # Подготавливаем название пакета
        label = package.replace('"', "#quot;")

        mermaid.append(
            f'    {node_id}["{label}"]'
        )

    # Добавляем связи между пакетами
    edge_number = 0
    cycle_edges = []

    for package, dependencies in graph.items():

        for dependency in dependencies:

            source = node_ids[package]
            target = node_ids[dependency]

            # Стрелка показывает связь зависимости
            mermaid.append(
                f"    {source} --> {target}"
            )

            # Запоминаем циклические связи
            if (package, dependency) in cycles:
                cycle_edges.append(edge_number)

            edge_number += 1

    # Задаём оформление вершин
    for package in packages:

        node_id = node_ids[package]

        mermaid.append(
            f"    style {node_id} "
            "fill:#d9ecff,stroke:#333,stroke-width:2px"
        )

    # Выделяем циклические связи красным цветом
    for edge_number in cycle_edges:

        mermaid.append(
            f"    linkStyle {edge_number} "
            "stroke:red,stroke-width:3px"
        )

    # Сохраняем текстовое представление Mermaid
    mermaid_path.write_text(
        "\n".join(mermaid),
        encoding="utf-8"
    )

    print(f"Mermaid-код сохранён: {mermaid_path}")

    
    # Задаём размеры изображения
    width = 1100
    height = 800

    # Считаем количество пакетов
    count = len(packages)

    # Находим центр изображения
    center_x = width // 2
    center_y = height // 2

    # Определяем радиус расположения вершин
    radius = min(width, height) // 2 - 120

    # Создаём словарь для хранения координат пакетов
    positions = {}

    # Располагаем вершины по кругу
    for i, package in enumerate(packages):

        # Вычисляем угол расположения вершины
        angle = 2 * math.pi * i / count - math.pi / 2

        # Вычисляем координаты вершины
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        # Сохраняем координаты пакета
        positions[package] = (x, y)

    # Создаём основу SVG-изображения
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',

        # Добавляем белый фон
        '<rect width="100%" height="100%" fill="white"/>',

        # Добавляем заголовок
        '<text x="550" y="40" text-anchor="middle" '
        'font-size="26" font-weight="bold">'
        'Граф зависимостей</text>',

        # Создаём стрелки для обозначения связей
        '<defs>'
        '<marker id="arrow" markerWidth="10" markerHeight="10" '
        'refX="8" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L9,3 z" fill="black"/>'
        '</marker>'
        '</defs>'
    ]

    # Рисуем связи между пакетами
    for package, dependencies in graph.items():

        x1, y1 = positions[package]

        for dependency in dependencies:

            x2, y2 = positions[dependency]

            # Если связь циклическая, окрашиваем её в красный цвет
            edge_color = (
                "red"
                if (package, dependency) in cycles
                else "black"
            )

            # Добавляем линию между вершинами
            svg.append(
                f'<line x1="{x1}" y1="{y1}" '
                f'x2="{x2}" y2="{y2}" '
                f'stroke="{edge_color}" stroke-width="2" '
                'marker-end="url(#arrow)"/>'
            )

    # Рисуем вершины и названия пакетов
    for package, (x, y) in positions.items():

        # Рисуем круг, обозначающий пакет
        svg.append(
            f'<circle cx="{x}" cy="{y}" r="40" '
            'fill="lightblue" stroke="black" '
            'stroke-width="2"/>'
        )

        # Добавляем название пакета
        svg.append(
            f'<text x="{x}" y="{y + 5}" '
            'text-anchor="middle" font-size="12">'
            f'{escape(package)}</text>'
        )

    # Закрываем SVG-изображение
    svg.append("</svg>")

    # Сохраняем SVG в файл
    output_path.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    print(f"SVG-граф сохранён: {output_path}")

#python -m src.main --stage 3 --package lodash --max-depth 2 --output dependencies-lodash.svg
#python -m src.main --stage 3 --package chalk --max-depth 2 --output dependencies-chalk.svg
#python -m src.main --stage 3 --package axios --max-depth 2 --output dependencies-axios.svg