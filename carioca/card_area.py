import gtk
import math

from carioca import HEARTS, CLUBS, DIAMONDS, SPADES

CARD_BASE_WIDTH  = 81
CARD_BASE_HEIGHT = 126

CARD_WIDTH  = 1 * CARD_BASE_WIDTH
CARD_HEIGHT = 1 * CARD_BASE_HEIGHT

class CardArea(gtk.DrawingArea):

	def __init__(self):
		gtk.DrawingArea.__init__(self)
		self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
		                gtk.gdk.BUTTON1_MOTION_MASK)

		self.connect('expose_event', self.expose)
		self.connect('button_press_event', self.pressing)
		self.connect('motion_notify_event', self.moving)

		self.desp = 0

		self.card_pixbuf = dict()
		self.initializeCards()

	def initializeCards(self):
		tmpbuf = gtk.gdk.pixbuf_new_from_file_at_size('/usr/share/gnome-games-common/cards/gnomangelo_bitmap.svg.unbranded', CARD_WIDTH*13, CARD_HEIGHT*5);

		# SVG contains from A to K horizontally,
		# and CL, DI, HE, SP and vertically
		j = 0
		for suit in CLUBS, DIAMONDS, HEARTS, SPADES:
			i = 0
			for rank in range(1,14):
				self.__read_card_pixbuf((rank, suit), tmpbuf, i, j)
				i += 1
			j += 1

		# Final line contains joker, double-joker and reverse
		self.__read_card_pixbuf((0, None), tmpbuf, 0, 4)
		self.__read_card_pixbuf('djkr', tmpbuf, 1, 4)
		self.__read_card_pixbuf('reverse', tmpbuf, 2, 4)

	def __read_card_pixbuf(self, key, source, x, y):
		self.card_pixbuf[key] = gtk.gdk.Pixbuf(
		                          source.get_colorspace(),
		                          source.get_has_alpha(),
		                          source.get_bits_per_sample(),
		                          CARD_WIDTH, CARD_HEIGHT)
		source.copy_area(x*CARD_WIDTH, y*CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT, self.card_pixbuf[key], 0, 0)

	###################
	# Signal handlers #
	###################
	def expose(self, widget, event):
		self.context = widget.window.cairo_create()
		self.context.rectangle(event.area.x, event.area.y,
		                       event.area.width, event.area.height)
		self.context.clip()
		self.draw(self.context)

	def draw(self, context):
		rect = self.get_allocation()

		# The green backgroung doesn't change
		context.rectangle(0, 0, rect.width, rect.height)
		context.set_source_rgb(0.0, 0.8, 0.0)
		context.fill_preserve()

		self.window.draw_pixbuf(None, self.card_pixbuf['reverse'], 0, 0, 0, 0, CARD_WIDTH, CARD_HEIGHT)

	def pressing(self, widget, event):
		# event has x,y of where it was produced
		pass

	def moving(self, widget, event):
		# event has x,y of where it was produced
		#
		# It also seems that this should be done at the end:
		#
		# self.draw(self.context)
		# self.queue_draw()
		pass
