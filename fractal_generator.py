from pencil import DrawingPencil

# Словарь l_systems_data содержит данные, используемые для создания объектов класса Fractal. Доступно 6 типов фракталов.
l_systems_data = {
    'Снежинка Коха':
        {'l_system': {'axiom': 'F--F--F', 'rules': {'F': 'F+F--F+F'}, 'angle': 60},
         'iter_opts': {2: [20, (-90, -30)], 3: [10, (-140, -75)], 4: [5, (-205, -120)]}},
    'Кристалл':
        {'l_system': {'axiom': 'F+F+F+F', 'rules': {'F': 'FF+F++F+F'}, 'angle': 90},
         'iter_opts': {2: [20, (-90, 100)], 3: [12, (-160, 160)], 4: [5, (-200, 205)]}},
    'Кольца':
        {'l_system': {'axiom': 'F+F+F+F', 'rules': {'F': 'FF+F+F+F+F+F-F'}, 'angle': 90},
         'iter_opts': {1: [25, (-20, 70)], 2: [15, (-15, 110)], 3: [9, (40, 190)]}},
    'Треугольник Серпинского':
        {'l_system': {'axiom': 'FXF--FF--FF', 'rules': {'F': 'FF', 'X': '--FXF++FXF++FXF--'}, 'angle': 60},
         'iter_opts': {2: [30, (-120, -90)], 3: [25, (-200, -160)], 4: [14, (-225, -190)], 5: [8, (-255, -215)]}},
    'Квадратный остров Коха':
        {'l_system': {'axiom': 'F+F+F+F', 'rules': {'F': 'F-F+F+FFF-F-F+F'}, 'angle': 90},
         'iter_opts': {1: [30, (-40, 80)], 2: [12, (-40, 140)], 3: [4, (-20, 195)]}},
    'Кривая Леви':
        {'l_system': {'axiom': 'F', 'rules': {'F': '+F--F+'}, 'angle': 45},
         'iter_opts': {5: [25, (-80, 65)], 6: [20, (-80, 80)], 7: [20, (-120, 90)], 8: [15, (-125, 90)],
                       9: [10, (-115, 90)], 10: [8, (-130, 90)]}},
}


class Fractal:
    def __init__(self, axiom: str, rules: dict, angle: int, distance: int, iters: int):
        """Класс-контейнер, содержащий информацию, необходимую для генерации фрактала."""
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.distance = distance
        self.iterations = iters


class FractalDrawer:
    __drawing_is_on = False  # Флаговая переменная, отражающая общее состояние рисования.

    def __init__(self, fractal: Fractal):
        """Класс, реализующий логику рисования фрактала."""
        self.__fractal = fractal
        self.__instructions = None

    def __create_instructions(self):
        """Создать строку инструкций для рисования."""
        start_string = self.__fractal.axiom
        end_string = ''
        # В данном цикле, на основе строк аксиомы и правил, генератор создает набор инструкций для черепашки.
        for _ in range(self.__fractal.iterations):
            end_string = ''.join(self.__fractal.rules[i] if i in self.__fractal.rules else i for i in start_string)
            start_string = end_string
        self.__instructions = end_string

    def draw_fractal(self, pen: DrawingPencil) -> bool:
        """Выполнить рисование по инструкции. Метод возвращает значение True, если рисование было завершено успешно
        или False, если оно было прервано."""

        # Вызовем метод, генерирующий строку инструкций для рисования.
        self.__create_instructions()
        # Перед началом рисования установим флаговой переменной значение True.
        FractalDrawer.__drawing_is_on = True

        # Каждому символу из набора инструкций в соответствие поставлена определенная команда из методов класса
        # RawTurtle: forward() - движение вперед на заданное кол-во пикселей, right() и left() - поворот
        # на заданное значение градусов вправо и влево соответственно.
        for cmd in self.__instructions:
            if FractalDrawer.__drawing_is_on:
                if cmd == 'F':
                    pen.forward(self.__fractal.distance)
                elif cmd == '+':
                    pen.right(self.__fractal.angle)
                elif cmd == '-':
                    pen.left(self.__fractal.angle)
            else:
                return False
        # После завершения рисования, возвращаем флаговой переменной значение False.
        FractalDrawer.__drawing_is_on = False

        return True
