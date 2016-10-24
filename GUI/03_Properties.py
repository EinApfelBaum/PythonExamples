import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


win = Gtk.Window()

label = Gtk.Label()
label.set_label("Go, Set the property label")
label.set_angle(12.5)
win.add(label)


print(label.get_properties("angle"))

widget = Gtk.Label()
print(dir(widget.props))


win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()




