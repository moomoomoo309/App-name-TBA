from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.label import Label
from kivy.properties import BoundedNumericProperty, StringProperty

topBarSize = 75
#The size of the top bar
CalWidget = None
CurrentMonth = "September"


class CalendarGrid(GridLayout):

    def __init__(self, **kwargs):
        super(CalendarGrid, self).__init__()  #I need this line for reasons.
        MonthLength = kwargs["MonthLength"]
        MonthStart = kwargs["MonthStart"]
        self.cols = 7
        self.rows = 6
        if MonthLength + MonthStart < 36:
            self.rows = 5
        #The grid is 7x6 because 7x5 isn't enough for months which start on Saturday
        self.spacing = 0
        #No spacing between each grid element is necessary.
        self.size = (Window.width, Window.height - topBarSize)
        #Keep it within its bounds.
        self.pos[1] -= 3
        self.pos[0] += 1
        self.spacing = 1
        #Center it a little nicer than kivy does by default.
        for i in range(0, MonthStart):
            self.add_widget(Widget())  #If the month doesn't start on a Monday, you need an empty day.
        for i in range(0, MonthLength):
            self.add_widget(ToggleButton(texture=None, background_normal="CalendarInactive.png",
                                         background_down="CalendarActive.png", group="CalendarGrid_Days",
                                         text="[color=000000][size=36]" + str(i + 1) + "[/color][/size]",
                                         pos=(0, Window.height - topBarSize), markup=True, halign="right",
                                         valign="top", text_size=(Window.width / 7, (Window.height - topBarSize) / 6)))
            #The group means they act as radio buttons, so only one is toggleable at a time.


def redraw(Window, width, height):
    global CalWidget
    CalWidget.canvas.clear()
    CalWidget.__init__(Month=CurrentMonth)
    return CalWidget


class CalendarWidget(Widget):
    Month = StringProperty("Month Name")

    def __init__(self, **kwargs):
        super(CalendarWidget, self).__init__()  #Still need this, apparently.
        with self.canvas:
            Rectangle(pos=(0, Window.height - topBarSize), size=(Window.width, topBarSize))  #Draw the top bar

        self.add_widget(Label(text_size=(Window.width, topBarSize), size=(Window.width, topBarSize),
                              text="[color=000000][size=36]" + kwargs["Month"] + "[/color][/size]",
                              pos=(0, Window.height - topBarSize), markup=True, halign="center", valign="middle"))
        #It's got markup in it for color and size, and the text is centered vertically and horizontally.
        #The text is from the keyword argument "Month".
        self.add_widget(CalendarGrid(MonthLength=31, MonthStart=1))
        #And this adds the grid.


class Calendar(App):
    def build(self):
        Window.bind(on_resize=redraw)
        global CalWidget
        CalWidget = CalendarWidget(Month=CurrentMonth)
        return CalWidget


if __name__ == "__main__":
    Calendar().run()