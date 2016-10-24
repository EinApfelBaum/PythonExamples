#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

loop = GObject.MainLoop()

GObject.threads_init()
Gst.init()
Gst.segtrap_set_enabled(False)

class Passthrough(Gst.Element):
    __gstmetadata__ = (
        "Passthrough element",
        "element.py",
        "Proxy buffers",
        "Andrew Cook <ariscop@gmail.com>"
    )

    _src_template = Gst.PadTemplate.new (
        'src',
        Gst.PadDirection.SRC,
        Gst.PadPresence.ALWAYS,
        Gst.caps_from_string('ANY')
    )
    _sink_template = Gst.PadTemplate.new (
        'sink',
        Gst.PadDirection.SINK,
        Gst.PadPresence.ALWAYS,
        Gst.caps_from_string('ANY')
    )

    _gsttemplates = (
        _src_template,
        _sink_template,
    )

    def __init__(self):
        Gst.Element.__init__(self)

        self.sinkpad = Gst.Pad.new_from_template(self._sink_template, 'sink')
        self.sinkpad.set_chain_function_full(self._sink_chain, None)
        self.sinkpad.set_event_function_full(self._sink_event, None)
        self.sinkpad.set_query_function_full(self._sink_query, None)
        self.add_pad(self.sinkpad)

        self.srcpad = Gst.Pad.new_from_template(self._src_template, 'src')
        self.srcpad.set_event_function_full(self._src_event, None)
        self.srcpad.set_query_function_full(self._src_query, None)
        self.add_pad(self.srcpad)

    def _sink_chain(self, pad, parent, buf):
        return self.srcpad.push(buf)

    def _src_event(self, pad, parent, event):
        return self.sinkpad.push_event(event)

    def _sink_event(self, pad, parent, event):
        return self.srcpad.push_event(event)

    # hack: force the query to be writable by messing with the refcount
    # https://bugzilla.gnome.org/show_bug.cgi?id=746329

    def _sink_query(self, pad, parent, query):
        refcount = query.mini_object.refcount
        query.mini_object.refcount = 1
        ret = self.srcpad.peer_query(query)
        query.mini_object.refcount += refcount - 1
        return ret

    def _src_query(self, pad, parent, query):
        refcount = query.mini_object.refcount
        query.mini_object.refcount = 1
        ret = self.sinkpad.peer_query(query)
        query.mini_object.refcount += refcount - 1
        return ret

GObject.type_register(Passthrough)

pipeline = Gst.Pipeline()

bus = pipeline.get_bus()
bus.add_signal_watch()

def connect(bus, name):
    def _connect(f):
        bus.connect(name, f)
        return f
    return _connect

@connect(bus, "message::warning")
def on_warning(bus, message):
    print(message.parse_warning())

@connect(bus, "message::info")
def on_info(bus, message):
    print(message.parse_info())

@connect(bus, "message::error")
def on_error(bus, message):
    pipeline.set_state(Gst.State.NULL)
    exit(message.parse_error())

source = Gst.ElementFactory.make("videotestsrc")
passthrough = Passthrough()
sink = Gst.ElementFactory.make("ximagesink")

pipeline.add(source)
pipeline.add(passthrough)
pipeline.add(sink)
source.link(passthrough)
passthrough.link(sink)

pipeline.set_state(Gst.State.PLAYING)

loop.run()