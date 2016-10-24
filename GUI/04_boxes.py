import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="A Button Sample")


        #Box
        self.box = Gtk.Box(spacing=10)
        self.add(self.box)

        # Bacon button
        self.bacon_button = Gtk.Button(label="Bacon")
        self.bacon_button.connect("clicked", self.button_clicked)
        self.box.pack_start(self.bacon_button, True, True, 0)

        # Tuna button
        self.tuna_button = Gtk.Button(label="Tuna")
        self.tuna_button.connect("clicked", self.button_clicked)
        self.box.pack_start(self.tuna_button, True, True, 0)


    def bacon_clicked(self, widget):
        print("I am a bacon")


    def tuna_clicked(self, widget):
        print("I am a tuna")

    def button_clicked(self, widget):
        name = widget.get_label()
        print(name)

win = MainWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()




