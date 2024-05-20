import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# class InfoWindow(Gtk.Dialog):
#     def __init__(self, info_text):
#         Gtk.Dialog.__init__(self, title="Information", transient_for=None, flags=0)
#
#         self.set_default_size(500, 400)
#
#         self.text_view = Gtk.TextView()
#         self.text_view.set_editable(False)
#         self.text_view.get_buffer().set_text(info_text)
#
#         scrolled_window = Gtk.ScrolledWindow()
#         scrolled_window.set_border_width(10)
#         scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
#         scrolled_window.add(self.text_view)
#
#         box = self.get_content_area()
#         box.add(scrolled_window)
#
#         self.show_all()

class InfoWindow(Gtk.Window):
    def __init__(self, info_text):
        Gtk.Window.__init__(self, title="Informacje")

        self.set_default_size(850, 500)

        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.get_buffer().set_text(info_text)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.text_view)

        self.add(scrolled_window)

        self.show_all()
