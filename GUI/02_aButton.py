import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="A Button Sample")

        # Button
        self.button = Gtk.Button(label="Click")
        self.button.connect("clicked", self.on_button_clicked)
        self.button.connect("leave", self.on_button_leave)
        self.button.connect("enter", self.on_button_enter)
        self.add(self.button)


    # User clicks button
    def on_button_clicked(self, widget):
        print("i was clicked.")

    def on_button_leave(self, widget):
        print("Something leaves")

    def on_button_enter(self, widget):
        print("Something enters")





win = MainWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()




