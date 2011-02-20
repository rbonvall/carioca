# encoding: utf-8
import gtk
import math

from carioca import HEARTS, CLUBS, DIAMONDS, SPADES

CARD_BASE_WIDTH  = 81
CARD_BASE_HEIGHT = 126

CARD_WIDTH  = 1 * CARD_BASE_WIDTH
CARD_HEIGHT = 1 * CARD_BASE_HEIGHT

class CardArea(gtk.DrawingArea):
	u'''
	The CardArea is a Drawing Area that shows the cards of a given game round.
	The area has a different layout depending on the name of players involved in the round, with a current maximum of 4 players allowed in the table.

	For 2 players, this is the layout of the card area:

	┌─────────────────────────────────┐
	│    ┌──────────────────────┐     │
	│    │   2nd player hand    │     │
	│    └──────────────────────┘     │
	│    ┌──────────────────────┐     │
	│    │   2nd player lowered │     │
	│    └──────────────────────┘     │
	│    ┌──────────────────────┐     │
	│    │      ┌─┐         ┌─┐ │     │
	│    │      │W│         │S│ │     │
	│    │      └─┘         └─┘ │     │
	│    └──────────────────────┘     │
	│    ┌──────────────────────┐     │
	│    │   1st player lowered │     │
	│    └──────────────────────┘     │
	│    ┌──────────────────────┐     │
	│    │   1st player hand    │     │
	│    └──────────────────────┘     │
	└─────────────────────────────────┘

	, where W and S are the well and the stack, respectivelly. When 3 players play,
	the layout is the following:

	┌────────────────────────────────────────────┐
	│┌──┐ ┌──┐                          ┌──┐ ┌──┐│
	││3 │ │3 │                          │2 │ │2 ││
	││r │ │r │                          │n │ │n ││
	││d │ │d │ ┌──────────────────────┐ │d │ │d ││
	││ h│ │ l│ │      ┌─┐         ┌─┐ │ │ l│ │ h││
	││ a│ │ o│ │      │W│         │S│ │ │ o│ │ a││
	││ n│ │ w│ │      └─┘         └─┘ │ │ w│ │ n││
	││ d│ │ .│ └──────────────────────┘ │ .│ │ d││
	││  │ │  │ ┌──────────────────────┐ │  │ │  ││
	││  │ │  │ │   1st player lowered │ │  │ │  ││
	│└──┘ └──┘ └──────────────────────┘ └──┘ └──┘│
	│          ┌──────────────────────┐          │
	│          │   1st player hand    │          │
	│          └──────────────────────┘          │
	└────────────────────────────────────────────┘

	Finally, then there are 4 players, the layout is the following:

	┌────────────────────────────────────────────┐
	│          ┌──────────────────────┐          │
	│          │   2nd player hand    │          │
	│          └──────────────────────┘          │
	│┌──┐ ┌──┐ ┌──────────────────────┐ ┌──┐ ┌──┐│
	││4 │ │4 │ │   2nd player lowered │ │2 │ │2 ││
	││t │ │t │ └──────────────────────┘ │n │ │n ││
	││h │ │y │ ┌──────────────────────┐ │d │ │d ││
	││ h│ │ l│ │      ┌─┐         ┌─┐ │ │ l│ │ h││
	││ a│ │ o│ │      │W│         │S│ │ │ o│ │ a││
	││ n│ │ w│ │      └─┘         └─┘ │ │ w│ │ n││
	││ d│ │ .│ └──────────────────────┘ │ .│ │ d││
	││  │ │  │ ┌──────────────────────┐ │  │ │  ││
	││  │ │  │ │   1st player lowered │ │  │ │  ││
	│└──┘ └──┘ └──────────────────────┘ └──┘ └──┘│
	│          ┌──────────────────────┐          │
	│          │   1st player hand    │          │
	│          └──────────────────────┘          │
	└────────────────────────────────────────────┘

	'''

	def __init__(self):
		gtk.DrawingArea.__init__(self)

		# Configure the widget
		self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
		                gtk.gdk.BUTTON1_MOTION_MASK)
		self.connect('expose_event', self.expose)
		self.connect('button_press_event', self.pressing)
		self.connect('motion_notify_event', self.moving)

		# Setup the inital facts
		self.nr_players = None
		self.game_round = None

		self.__initializeCards()

	def __initializeCards(self):

		self.card_pixbuf = dict()
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

		# We need the rotated 'reverse' cards to show for the other players
		self.card_pixbuf['reverse-cw']  = self.card_pixbuf['reverse'].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE)
		self.card_pixbuf['reverse-ccw'] = self.card_pixbuf['reverse'].rotate_simple(gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE)

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

	##################
	# Drawing method #
	##################
	def draw(self, context):
		rect = self.get_allocation()

		# The green backgroung doesn't change
		context.rectangle(0, 0, rect.width, rect.height)
		context.set_source_rgb(0.0, 0.8, 0.0)
		context.fill_preserve()

		# Draw the different sets of cards
		if self.game_round:
			self.__draw_well_and_stack()
			self.__draw_local_player()
			self.__draw_other_players()

	def __draw_well_and_stack(self):
		self.__draw_card(self.game_round.peek_well_card(), 100, 100)
		self.__draw_card('reverse', 200, 100)

	def __draw_local_player(self):
		pass

	def __draw_other_players(self):
		pass

	def __draw_card(self, card, x, y, orientation=gtk.gdk.PIXBUF_ROTATE_NONE):
		if orientation == gtk.gdk.PIXBUF_ROTATE_NONE:
			self.window.draw_pixbuf(None, self.card_pixbuf[card], 0, 0, x, y, CARD_WIDTH, CARD_HEIGHT)
		else:
			self.window.draw_pixbuf(None, self.card_pixbuf[card], 0, 0, x, y, CARD_HEIGHT, CARD_WIDTH)

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

	##########
	# Others #
	##########
	def set_game_round(self, game_round):
		self.game_round = game_round
		self.queue_draw()

	def set_nr_players(self, nr_players):
		self.nr_players = nr_players
