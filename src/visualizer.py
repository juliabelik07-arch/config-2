# ЭТАП 3. Визуализация графа зависимостей
# Файл отвечает за создание изображения графа в формате SVG.

import math
from pathlib import Path
from xml.sax.saxutils import escape


# Функция построения и сохранения графа
def visualize_graph(graph, cycles, output):

    # Задаём размеры изображения
    width = 900
    height = 700

    # Получаем список всех пакетов
    packages = list(graph.keys())

    # Считаем количество пакетов
    count = len(packages)

    # Проверяем, что граф не пустой
    if count == 0:
        raise RuntimeError("Граф пустой")

    # Находим центр изображения
    center_x = width // 2
    center_y = height // 2

    # Определяем радиус расположения вершин
    radius = min(width, height) // 2 - 100

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
        f'width="{width}" height="{height}">',

        # Добавляем белый фон
        '<rect width="100%" height="100%" fill="white"/>',

        # Добавляем заголовок
        '<text x="450" y="35" text-anchor="middle" '
        'font-size="24">Граф зависимостей</text>'
    ]

    # Рисуем связи между пакетами
    for package, dependencies in graph.items():

        # Получаем координаты текущего пакета
        x1, y1 = positions[package]

        # Перебираем его зависимости
        for dependency in dependencies:

            # Пропускаем пакеты, которых нет среди вершин
            if dependency not in positions:
                continue

            # Получаем координаты зависимости
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
                f'stroke="{edge_color}" stroke-width="2"/>'
            )

    # Рисуем вершины и названия пакетов
    for package, (x, y) in positions.items():

        # Рисуем круг, обозначающий пакет
        svg.append(
            f'<circle cx="{x}" cy="{y}" r="30" '
            'fill="lightblue" stroke="black" stroke-width="2"/>'
        )

        # Добавляем название пакета внутри круга
        svg.append(
            f'<text x="{x}" y="{y + 5}" '
            'text-anchor="middle" font-size="14">'
            f'{escape(package)}</text>'
        )

    # Закрываем SVG-изображение
    svg.append("</svg>")

    # Создаём путь к выходному файлу
    output_path = Path(output)

    # Создаём папку, если её ещё нет
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем SVG в файл
    output_path.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    # Выводим сообщение о сохранении
    print(f"\nГраф сохранён в файл: {output_path}")
