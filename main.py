from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    V_NB_LINES = 12
    V_LINES_SPACCING = .2
    vertical_line = []

    H_NB_LINES = 10
    H_LINES_SPACCING = .1
    horizontale_line = []
    current_offset_y = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()
        Clock.schedule_interval(self.update, 1.0/60.0)

    def on_parent(self, widget, parent):
        print("On PARENT W: " + str(self.width) + " H: " + str(self.height))

    def on_size(self, *args):
        pass
        # self.update_vertical_line()
        # self.update_horizontal_line()
        # print("ON SIZE  W: " + str(self.width) + " H: " + str(self.height))
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.height * 0.75

    def on_perspective_point_x(self, widget, value):
        print("PX : " + str(value))

    def on_perspective_point_y(self, widget, value):
        print("PY : " + str(value))

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_line.append(Line())

    def update_vertical_line(self):
        # self.line.points = [self.perspective_point_x,  0, self.perspective_point_x, 100]
        central_line = self.width / 2
        spaccing = self.V_LINES_SPACCING * self.width
        offset = -int(self.V_NB_LINES / 2) + 0.5
        for i in range(0, self.V_NB_LINES):
            line_x = int(central_line + offset * spaccing)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_line[i].points = [x1, y1, x2, y2]
            offset += 1

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.H_NB_LINES):
                self.horizontale_line.append(Line())

    def update_horizontal_line(self):
        central_line = self.width / 2
        spaccing = self.V_LINES_SPACCING * self.width
        offset = -int(self.V_NB_LINES / 2) + 0.5

        xmin = central_line + offset * spaccing
        xmax = central_line - offset * spaccing

        spaccing_y = self.H_LINES_SPACCING * self.height
        for i in range(0, self.H_NB_LINES):
            line_y = i * spaccing_y + self.current_offset_y
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontale_line[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        return self.transform_2D(x, y)
        # return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return x, y

    def transform_perspective(self, x, y):
        line_y = y * self.perspective_point_y / self.height
        if line_y > self.perspective_point_y:
            line_y = self.perspective_point_y

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - line_y
        factory_y = diff_y / self.perspective_point_y
        factory_y = pow(factory_y, 4)
        offset_x = diff_x * factory_y
        tr_x = self.perspective_point_x + offset_x
        tr_y = self.perspective_point_y - factory_y * self.perspective_point_y
        return tr_x, tr_y

    def update(self, dt):
        self.update_vertical_line()
        self.update_horizontal_line()
        self.current_offset_y -= 1


class GalaxyApp(App):
    pass


GalaxyApp().run()
