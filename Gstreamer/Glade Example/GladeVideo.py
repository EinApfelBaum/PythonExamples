#!/usr/bin/python3

from os import path

import gi
from gi.repository import GstPbutils

gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('GdkX11', '3.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, Gtk, GdkX11, GstVideo, GLib
import random
import time

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:


GObject.threads_init()
Gst.init(None)
filename = "/home/baum/Videos/test/Big_Buck_Bunny_12.09.30_02-25_osf_10_TVOON_DE.mpg.HQ.avi"
uri = 'file://' + filename

class Player(object):
    def __init__(self):
        self.marker_a, self.marker_b = 0, -1
        self.timelines = [[]]
        self.cut_selected = -1
        self.timer = None
        self.hide_cuts = False
        self.frames = 0
        self.slider = None
        self.keyframes = None
        self.videolength = 0

        self.getVideoLength = True

        self.builder = Gtk.Builder()
        self.builder.add_from_file("video.glade")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window1")
        self.window.connect('destroy', self.quit)
        self.window.set_default_size(800, 450)

        self.drawingarea = self.builder.get_object("drawingarea1")


        self.drawingarea.connect('realize', self.on_realize)
        self.drawingarea.connect('unrealize', self.on_unrealize)

        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)
        self.bus.connect('message', self.on_message)

        # Create GStreamer elements
        self.playbin = Gst.ElementFactory.make('playbin', None)

        # Add playbin to the pipeline
        self.pipeline.add(self.playbin)

        # Set properties
        self.playbin.set_property('uri', uri)

        self.pipeline.set_state(Gst.State.PLAYING)
        self.pipeline.set_state(Gst.State.PAUSED)

        discover = GstPbutils.Discoverer.new(Gst.SECOND)
        self.d = discover.discover_uri(uri)
        print('# video')
        for vinfo in self.d.get_video_streams():
            self.framerate_num = vinfo.get_framerate_num()
            self.framerate_denom = vinfo.get_framerate_denom()
            print(vinfo.get_caps().to_string().replace(', ', '\n\t'))

        # Slider

        self.slider = self.builder.get_object("scale1")

    def on_realize(self, widget, data=None):
        print("on_realize")

        window = widget.get_window()
        self.xid = window.get_xid()
        self.playbin.set_window_handle(self.xid)

    def on_draw(self, widget, cr):
        print("ondraw", self.playbin.get_state(0).state)
        if self.playbin.get_state(0).state < Gst.State.PAUSED:
            allocation = widget.get_allocation()

            cr.set_source_rgb(0, 0, 0)
            cr.rectangle(0, 0, allocation.width, allocation.height)
            cr.fill()

        self.on_realize(widget)


    def on_unrealize(self, widget, data=None):
        # to prevent racing conditions when closing the window while playing
        self.playbin.set_state(Gst.State.NULL)



    def run(self):
        self.window.show_all()
        # You need to get the XID after window.show_all().  You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there.
        self.xid = self.drawingarea.get_property('window').get_xid()
        print(self.xid)
        Gtk.main()

    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)
            #print(msg.src.set_window_handle(self.xid))
            print(msg)
            print(msg.get_structure())

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.ASYNC_DONE:
            if self.getVideoLength is True:
                self.getVideoLength = False
                print('Async done')
                self.videolength = self.playbin.query_duration(Gst.Format.TIME)
                self.frames = self.videolength[1] * self.framerate_num / self.framerate_denom / Gst.SECOND
                self.slider.set_range(0, self.get_frames())

    def on_eos(self, bus, msg):
        print('on_eos(): seeking to start of video')
        self.pipeline.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())

    def on_playButtonClicked(self, button):
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_pauseButtonClicked(self, button):
        self.pipeline.set_state(Gst.State.PAUSED)

    def on_btnFrameFastBackwardClicked(self, button):
        print('Frame Backward: ')
        self.jump_relative(-1)

    def on_btnKeyFastBackwardClicked(self, button):
        print('Key Frame Backward: ')

    def on_btnFFastBackwardClicked(self, button):
        print('FFast Backward: ')
        self.jump_relative(-100)

    def on_btnFastBackwardClicked(self, button):
        print('Fast Backward: ')
        self.jump_relative(-10)

    def on_btnFastForwardClicked(self, button):
        print('Fast Forward: ')
        self.jump_relative(10)

    def on_btnFFastForwardClicked(self, button):
        print('FFast Forward: ')
        self.jump_relative(100)

    def on_btnKeyFastForwardClicked(self, button):
        print('KeyFrame Fast Forward: ')

    def on_btnFrameFastForwardClicked(self, button):
        print('Frame Fast Forward: ')
        self.jump_relative(1)

    def on_valueChanged(self, range):
        # print("value changed")

        frames = self.slider.get_value()
        self.slider.set_fill_level(frames)
        print(frames)
        if frames >= self.get_frames():
            print("restrict")
            frames = self.get_frames() - 1
        self.playbin.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
                                 frames * Gst.SECOND * self.framerate_denom / self.framerate_num)

    def jump_relative(self, frames, flags=Gst.SeekFlags.ACCURATE):
        try:
            nano_seconds = self.playbin.query_position(Gst.Format.TIME)[1]


        except Exception as e:
            # time.sleep(0.04)
            nano_seconds = self.playbin.query_position(Gst.Format.TIME)[1]

        print("act pos: ", nano_seconds, " ns")
        nano_seconds += frames * (1 * Gst.SECOND * self.framerate_denom / self.framerate_num)
        print("new pos: ", nano_seconds, " ns")

        if nano_seconds < 0:
            print("restrict")
            nano_seconds = 0
        elif nano_seconds * self.framerate_num / self.framerate_denom / Gst.SECOND >= self.get_frames():
            print("restrict")
            nano_seconds = (self.get_frames() - 1) * Gst.SECOND * self.framerate_denom / self.framerate_num

        self.jump_to(nanoseconds=nano_seconds, flags=flags)

    def jump_to(self, frames=None, seconds=None, nanoseconds=0, flags=Gst.SeekFlags.ACCURATE):
        if frames:
            if frames >= self.get_frames():
                frames = self.get_frames() - 1

            nanoseconds = frames * Gst.SECOND * self.framerate_denom / self.framerate_num
        elif seconds:
            nanoseconds = seconds * Gst.SECOND

        self.playbin.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | flags, int(nanoseconds))

    def get_frames(self):
        """ Returns the current number of frames to be shown. """
        if self.hide_cuts:
            frames = sum([duration for start, duration in self.timelines[-1]])
        else:
            frames = self.frames

        return frames



p = Player()
p.run()


