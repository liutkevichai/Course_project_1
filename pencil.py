from turtle import RawTurtle # Импорт класса «черепахи» из модуля стандартной библиотеки.


class DrawingPencil(RawTurtle):  # Наследует свойства родительского класса RawTurtle.
    def __init__(self, canvas):
        """Создает "карандаш" с заданными настройками для рисования черепашьей графики на полотне виджета Canvas
        из модуля Tkinter."""
        super().__init__(canvas)
        self.color('white')
        self.speed(0)
        self.hideturtle()

    def setpos(self, coords: tuple):  # Переопределяет метод setpos() родительского класса.
        """Перенести "карандаш" в заданную точку. Принимает в качестве аргумента кортеж с координатами (x, y)."""
        self.pu()
        super().setpos(coords)
        self.pd()

    def set_color(self, pencolor: str):
        """Изменить цвет рисования."""
        self.color(pencolor)
