import random
import math

class Dot():
    def __init__(self, screen_width, screen_height,
        start_x=None, start_y=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = random.randint(1, 3)
        sides = ["left", "right", "top", "bottom"]

        #Определение стартовых координат
        if start_x is not None and start_y is not None:
            #Координаты переданы
            self.x = float(start_x)
            self.y = float(start_y)
        else:
            #Координаты не переданы, генерация точки на одной из сторон
            #Выбор стороны для стартовой точки
            self.start_side = random.choice(sides)
            sides.remove(self.start_side)
            #Получение координат стартовой точки
            self.x, self.y = self.get_coords_on_side(self.start_side)
            self.x = float(self.x)
            self.y = float(self.y)

        #Получение стороны для конечной точки
        self.target_side = random.choice(sides)
        #Получение координат конечной точки
        self.target_x, self.target_y = self.get_coords_on_side(self.target_side)
        
        #Получение единичного вектора
        self.unit_vector = self.calculate_unit_vector()


    def get_coords_on_side(self, side):
        """Генерирует случайные координаты на указанной стороне экрана
        Args: side (str): сторона экрана
        Returns: кортеж с координатами (x, y)
        """
        MARGIN = 10 #Отступ от краев экрана, мертвая зона
        EXTRA = 5 #Отступ от края за пределы экрана, для появления и удаления точки за его видимой частью
        match side:
            case "top":
                return random.randint(MARGIN, self.screen_width-MARGIN), -EXTRA
            case "bottom":
                return random.randint(MARGIN, self.screen_width-MARGIN), self.screen_height+EXTRA
            case "left":
                return -EXTRA, random.randint(MARGIN, self.screen_height-MARGIN)
            case "right":
                return self.screen_width+EXTRA , random.randint(MARGIN, self.screen_height-MARGIN)
            case _:
                raise ValueError("Invalid value of 'side', use top, bottom, left, right")

    def calculate_unit_vector(self):
        """Функция для получения единичного вектора"""
        #Координаты вектора
        self.vector = ((self.target_x - self.x), (self.target_y - self.y))

        #Длина вектора sqrt(v1^2+v2^2)
        length=math.sqrt(self.vector[0]**2 + self.vector[1]**2)

        #Единичный вектор
        unit_vector=(round(self.vector[0] / length, 2), round(self.vector[1] / length, 2))
        return unit_vector


    def move(self):
        """Функция перемещает точку на один шаг в направление вектора"""
        self.x += self.unit_vector[0] * self.speed
        self.y += self.unit_vector[1] * self.speed


    def is_beyond_target_boundary(self):
        """Проверяет, вышла ли точка за границу экрана на основе target_side"""
        RADIUS = 5 #Приблизительный радиус точки (точка пропадала после полного исчезновения с экрана)
        match self.target_side:
            case "top":
                return self.y < -RADIUS
            case "bottom":
                return self.y > self.screen_height+RADIUS
            case "left":
                return self.x < -RADIUS
            case "right":
                return self.x > self.screen_width+RADIUS


    def print_info(self):
        """Возвращает состояние объекта Dot"""
        print(f"Start side: {self.start_side}")
        print(f"Target side: {self.target_side}")
        print(f"Position: x: {self.x}, y: {self.y}")
        print(f"Target: x: {self.target_x}, y: {self.target_y}")
        print(f"Unit vector: [{self.unit_vector[0]}, {self.unit_vector[1]}]")


"""TODO: 
- векторная математика, повторить основы, базовый, единичный вектор
"""