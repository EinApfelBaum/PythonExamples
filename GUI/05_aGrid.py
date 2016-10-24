import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="A Button Sample")

        grid = Gtk.Grid()
        self.add(grid)


        # some buttons
        button1 = Gtk.Button(label="Button1")
        button2 = Gtk.Button(label="Button2")
        button3 = Gtk.Button(label="Button3")
        button4 = Gtk.Button(label="Button4")
        button5 = Gtk.Button(label="Button5")
        button6 = Gtk.Button(label="Button6")
        button7 = Gtk.Button(label="Button7")

        grid.add(button1)
        grid.attach(button2, 1, 0, 1, 1)
        grid.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach(button4, 1, 1, 2, 2)
        grid.attach(button5, 2, 0, 1, 1)
        grid.attach(button6, 0, 2, 1, 1)
        grid.attach(button7, 0, 3, 1, 1)

win = MainWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()




