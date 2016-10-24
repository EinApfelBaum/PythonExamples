
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MyBox(Gtk.HBox):
       __gtype_name__ = 'MyBox'

       def __init__(self):
               Gtk.HBox.__init__(self)