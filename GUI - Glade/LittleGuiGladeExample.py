import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")

builder = Gtk.Builder()
builder.add_from_file("builder_example.glade")
builder.connect_signals(Handler())
button1 = builder.get_object("button1")
builder.get_object("comboboxtext1").append_text("Test")
cb = builder.get_object("comboboxtext1")
cb.append_text("test2")
cb.insert_text(0,"test3")
cb.insert_text(0,"test5")
cb.prepend_text("hallo")
cb.insert_text(0,"Test")




window = builder.get_object("window1")
window.show_all()


Gtk.main()
