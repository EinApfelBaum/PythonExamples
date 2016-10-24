import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio
import sys


class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Toolbar Example", application=app)
        self.set_default_size(400, 200)

        # a grid to attach the toolbar (see below)
        grid = Gtk.Grid()
        self.add(grid)
        # we have to show the grid (and therefore the toolbar) with show(),
        # as show_all() would show also the buttons in the toolbar that we want to
        # be hidden (such as the leave_fullscreen button)
        grid.show()

        # a builder to add the UI designed with Glade to the grid:
        builder = Gtk.Builder()
        # get the file (if it is there)
        try:
            builder.add_from_file("toolbar_builder.glade")
        except:
            print("file not found")
            sys.exit()
        # and attach it to the grid
        grid.attach(builder.get_object("toolbar"), 0, 0, 1, 1)

        # two buttons that will be used later in a method
        self.fullscreen_button = builder.get_object("fullscreen_button")
        self.leave_fullscreen_button = builder.get_object(
            "leave_fullscreen_button")

        # create the actions that control the window, connect their signal to a
        # callback method (see below), add the action to the window:

        # undo
        undo_action = Gio.SimpleAction.new("undo", None)
        undo_action.connect("activate", self.undo_callback)
        self.add_action(undo_action)

        # and fullscreen
        fullscreen_action = Gio.SimpleAction.new("fullscreen", None)
        fullscreen_action.connect("activate", self.fullscreen_callback)
        self.add_action(fullscreen_action)

        # hide button
        self.toolbutton = builder.get_object("new_button")
        self.toolbutton.hide()



    # callback for undo
    def undo_callback(self, action, parameter):
        print("You clicked \"Undo\".")

    # callback for fullscreen
    def fullscreen_callback(self, action, parameter):
        # check if the state is the same as Gdk.WindowState.FULLSCREEN, which
        # is a bit flag
        is_fullscreen = self.get_window().get_state(
        ) & Gdk.WindowState.FULLSCREEN != 0
        if is_fullscreen:
            self.unfullscreen()
            self.leave_fullscreen_button.hide()
            self.fullscreen_button.show()
        else:
            self.fullscreen()
            self.fullscreen_button.hide()
            self.leave_fullscreen_button.show()


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        # show the window - with show() not show_all() because that would show also
        # the leave_fullscreen button
        win.show()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # actions that control the application: create, connect their signal to a
        # callback method (see below), add the action to the application

        # new
        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.new_callback)
        app.add_action(new_action)

        # open
        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.open_callback)
        app.add_action(open_action)

    # callback for new
    def new_callback(self, action, parameter):
        print("You clicked \"New\".")

    # callback for open
    def open_callback(self, action, parameter):
        print("You clicked \"Open\".")

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)