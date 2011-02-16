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

		i = 0
		for suit in CLUBS, DIAMONDS, HEARTS, SPADES:
			j = 0
			for rank in range(1,14):
				card = (rank, suit)
				self.card_pixbuf[card] = gtk.gdk.Pixbuf(
				                          tmpbuf.get_colorspace(),
				                          tmpbuf.get_has_alpha(),
				                          tmpbuf.get_bits_per_sample(),
				                          CARD_WIDTH, CARD_HEIGHT)
				tmpbuf.copy_area(j*CARD_WIDTH, i*CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT, self.card_pixbuf[card], 0, 0)
				j += 1
			i += 1

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
		x = rect.x + rect.width / 2
		y = rect.y + rect.height / 2
		
		radius = min(rect.width / 2, rect.height / 2) - 5
		
		context.arc(x, y, radius, 0 + self.desp, (1 * math.pi) + self.desp)
		
		context.set_source_rgb(0.7, 0.8, 0.1)
		context.fill_preserve()
		
		context.set_source_rgb(0, 0, 0)
		context.stroke()

		#self.cardpixbuf.render_to_drawable(self,context, 0, 0, 0, 0, 0, 0, 0)
		self.window.draw_pixbuf(None, self.card_pixbuf[(6, SPADES)], 0, 0, 0, 0, CARD_WIDTH, CARD_HEIGHT)

	def pressing(self, widget, event):
		self.pressing_x = event.x

	def moving(self, widget, event):

		if(self.pressing_x - event.x) > 1:
			self.desp = self.desp + 0.1
		else:
			self.desp = self.desp - 0.1

		self.pressing_x = event.x

		self.draw(self.context)
		self.queue_draw()
