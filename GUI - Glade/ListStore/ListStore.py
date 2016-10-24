import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")

builder = Gtk.Builder()
builder.add_from_file("ListStore.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.set_default_size(400, 200)
window.show_all()

liststore = builder.get_object("liststore1")

liststore.append(["eins", "zwei"])
liststore.append(["drei", "zwei"])
liststore.append(["vier", "zwei"])



for row in liststore:
    print(row[:])


Gtk.main()