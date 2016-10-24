import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gtk
from gi.repository import Gst as gst

'''
The following 2 lines are required for gstreamer => 1.0
to initialize the GObject.
'''
GObject.threads_init()
gst.init(None)

# Create the pipeline for our elements.
'''
pipeline = gst.Pipeline('pipeline')
gst.Pipeline()
replaced
with "Null" parameter in gstreamer = > 1.0
'''
pipeline = gst.Pipeline()
# Create the elements for our project.

'''
gst.element_factory_make = > gst.ElementFactory.make
'''
audio_source = gst.ElementFactory.make('filesrc', 'audio_source')
decode = gst.ElementFactory.make('mad', 'decode')
convert = gst.ElementFactory.make('audioconvert', 'convert')
equalizer = gst.ElementFactory.make('equalizer-3bands', 'equalizer')
audio_sink = gst.ElementFactory.make('autoaudiosink', 'audio_sink')

# Ensure all elements were created successfully.
if (not pipeline or not audio_source or not decode or not convert or not equalizer or not audio_sink):
    print('Not all elements could be created.')
    exit(-1)

# Configure our elements.
audio_source.set_property('location', '1.mp3')
equalizer.set_property('band1', -24.0)
equalizer.set_property('band2', -24.0)

# Add our elements to the pipeline.
'''
pipeline.add(audio_source, decode, convert, equalizer, audio_sink)
no longer available in Gst - 0.10 in gstreamer = > 1.0
you need to add them on by one and ordering counts.
'''
pipeline.add(audio_source)
pipeline.add(decode)
pipeline.add(convert)
pipeline.add(equalizer)
pipeline.add(audio_sink)

# Link our elements together.
'''
gst.element_link_many(audio_source, decode, convert, equalizer, audio_sink)):
= > no longer  available in gstreamer = > 1.0
you need to use link() which links two parameter.
'''
audio_source.link(decode)
decode.link(convert)
convert.link(equalizer)
equalizer.link(audio_sink)

# Set our pipelines state to Playing.
'''
gst.STATE_PLAYING = > gst.State.PLAYING

Just a hint: check the following documentation whenever you get some
AttributeError.
    link: http: // lazka.github.io / pgi - docs /  # Gst-1.0/flags.html

'''
pipeline.set_state(gst.State.PLAYING)

# Wait until error or EOS.
bus = pipeline.get_bus()


'''
Following
are
also
changed in gstreamer = > 1.0
gst.MESSAGE_ERROR = > gst.MessageType.ERROR
gst.MESSAGE_EOS = > gst.MessageType.EOS
'''
msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,gst.MessageType.ERROR | gst.MessageType.EOS)
print(msg)

# Free resources.
pipeline.set_state(gst.State.NULL)