# Импортируем требуемый функционал из модуля tkinter и пользовательские модули.
from tkinter import Tk, Canvas, Frame, Menu, Button, Label
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from fractal_generator import *

BACKGROUND = 'black'
COLORS = ['red', 'orange', 'yellow', 'green', 'deep sky blue', 'blue', 'dark orchid']


class GUI:
    def __init__(self):
        # Создаем и настраиваем окно программы, виджет Tk.
        self.window = Tk()
        self.window.geometry('700x700')
        self.window.title('Генератор фракталов')
        self.window.resizable(width=False, height=False)
        self.window.config(bg=BACKGROUND)

        # Создаем и настраиваем меню 'О программе' - виджет Menu.
        self.menubar = Menu()
        self.window.config(menu=self.menubar)
        self.about = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='О программе', menu=self.about)
        self.about.add_command(
            label='Справка',
            command=lambda ttl='Справка', msg='Курсовой проект по предмету '
                                              '"Объектно-ориентированное программирование"': showinfo(ttl, msg)
        )
        self.about.add_command(
            label='О разработчике',
            command=lambda ttl='О разработчике', msg='''
                                Автор: А.И.Люткевич
                                Группа: з-423П2-4
                                Кафедра АОИ
                                Направление подготовки 09.03.04
                                ''': showinfo(ttl, msg)
        )

        # Создаем и настраиваем полотно - виджет Canvas.
        self.canvas = Canvas(master=self.window, highlightthickness=0)
        self.canvas.config(width=700, height=515)
        self.canvas.grid(row=1, column=0)

        # Создаем и настраиваем кнопки выбора цвета и подпись к ним, помещаем их в виджет Frame.
        self.frm_colors = Frame(master=self.window, bg=BACKGROUND)
        self.frm_colors.grid(row=0, column=0)
        self.label = Label(master=self.frm_colors, fg='white', bg=BACKGROUND,
                           font=('Courier', 18, 'normal'), text='Выберите цвет рисования:')
        self.label.grid(row=0, column=0, columnspan=7, pady=15, sticky='n')
        self.create_color_buttons()

        # Создаем и настраиваем кнопки фракталов, помещаем их в виджет Frame.
        self.frm_fractals = Frame(master=self.window, bg=BACKGROUND)
        self.frm_fractals.grid(row=2, column=0)
        self.create_fractal_buttons()

        # Создаем новый объект класса Pencil, настраиваем цвет 'полотна'.
        self.pencil = DrawingPencil(self.canvas)
        self.canvas.config(bg=BACKGROUND)

        # Основной цикл событий.
        self.window.mainloop()

    def create_color_buttons(self):
        """Cоздает кнопки для каждого из цветов в списке COLORS."""
        for i, color in enumerate(COLORS):
            fractal_button = Button(master=self.frm_colors, bg=color, width=2,
                                    command=lambda c=color: self.pencil.set_color(c))
            fractal_button.grid(row=1, column=i, padx=25)

    def create_fractal_buttons(self):
        """Создает 6 кнопок для фракталов разных типов."""
        fractal_buttons = []
        for i in range(2):
            for j in range(3):
                fractal_button = Button(master=self.frm_fractals, width=25)
                fractal_button.grid(row=i, column=j, padx=10, pady=8)
                fractal_buttons.append(fractal_button)

        for i, button in enumerate(fractal_buttons):
            fractal_name = list(l_systems_data.keys())[i]
            button.config(text=fractal_name, command=lambda name=fractal_name: self.draw_new_fractal(name))

    def draw_new_fractal(self, fractal_name: str):
        """Создать новый объект класса Fractal и запустить его рисование. В качестве аргумента функция принимает
        название фрактала, являющееся ключом словаря l_systems_data из модуля fractal_generator."""

        # Получаем словарь choice, являющийся значением для выбранного фрактала в словаре l_systems.
        choice = l_systems_data[fractal_name]
        iter_options = choice['iter_opts'].keys()

        # Диалоговое окно предлагает пользователю выбрать кол-во итераций из доступных для данного фрактала.
        try:
            iters = int(askstring(title='Кол-во итераций',
                              prompt=f'Введите количество итераций от {min(iter_options)} до {max(iter_options)}.'))
        except ValueError:
            showinfo(title='Ошибка', message='Введите целое число из предложенного диапазона.')

        # Проверяем, доступно ли выбранное пользователем кол-во итераций.
        if iters in choice['iter_opts'].keys():
            # Удаляем предыдущий рисунок, устанавливаем 'карандаш' в начальную позицию.
            self.pencil.clear()
            self.pencil.setheading(0)
            self.pencil.setpos(choice['iter_opts'][iters][1])

            # Настройка надписи над кнопками выбора цвета.
            self.label.config(text='Выберите цвет рисования:')

            # Создаем новый объект класса Fractal, инициализируем его атрибуты значениями из словаря и кол-вом итераций.
            fractal = Fractal(**choice['l_system'], distance=choice['iter_opts'][iters][0], iters=int(iters))

            fractal_drawer = FractalDrawer(fractal)
            # Запускаем рендеринг фрактала. Если он был успешно завершен, надпись отобразит кол-во итераций.
            if fractal_drawer.draw_fractal(self.pencil):
                self.label.config(text=f'Готово! Кол-во итераций: {iters}')

        # Если пользователь ввел недоступное количество итераций, будет выведено сообщение об ошибке.
        else:
            showinfo(title='Ошибка', message='Выбрано недоступное количество итераций.')


if __name__ == '__main__':
    program_interface = GUI()
