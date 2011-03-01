# encoding: utf-8
import cairo
import gtk

from carioca import HEARTS, CLUBS, DIAMONDS, SPADES
from collections import namedtuple

# Cards have a 9:14 ratio
CARD_BASE_WIDTH  = 9
CARD_BASE_HEIGHT = 14

CARD_WIDTH  = 7 * CARD_BASE_WIDTH
CARD_HEIGHT = 7 * CARD_BASE_HEIGHT

# Areas where cards are shown are always CARD_HEIGHT in the short side
# and AREAS_LONGSIDE in the long side
AREAS_LONGSIDE = 4 * CARD_WIDTH

# Other distances
TOP_BOTTOM_PADDING       = 5
LEFT_RIGHT_PADDING       = 5
INTER_AREAS_PADDING      = 5
STACK_AREA_VERT_PADDING  = 5
STACK_AREA_HORIZ_PADDING = 5
STACK_WELL_SEPARATION    = 5

# Used to store (x,y) coordinates
Coordinates = namedtuple('Coordinates', 'x y')

def round_rectangle(context, x,y,w,h,r = 10):
	'''Draw a rounded rectangle in the given cairo context'''
	#   A****BQ
	#  H      C
	#  *      *
	#  G      D
	#   F****E
	context.move_to(x+r,y)                      # Move to A
	context.line_to(x+w-r,y)                    # Straight line to B
	context.curve_to(x+w,y,x+w,y,x+w,y+r)       # Curve to C, Control points are both at Q
	context.line_to(x+w,y+h-r)                  # Move to D
	context.curve_to(x+w,y+h,x+w,y+h,x+w-r,y+h) # Curve to E
	context.line_to(x+r,y+h)                    # Line to F
	context.curve_to(x,y+h,x,y+h,x,y+h-r)       # Curve to G
	context.line_to(x,y+r)                      # Line to H
	context.curve_to(x,y,x,y,x+r,y)             # Curve to A
	context.close_path()


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
		self.__initializeCairo()

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
		self.card_pixbuf['reverse-ud']  = self.card_pixbuf['reverse'].rotate_simple(gtk.gdk.PIXBUF_ROTATE_UPSIDEDOWN)
		self.card_pixbuf['reverse-cw']  = self.card_pixbuf['reverse'].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE)
		self.card_pixbuf['reverse-ccw'] = self.card_pixbuf['reverse'].rotate_simple(gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE)

	def __read_card_pixbuf(self, key, source, x, y):
		self.card_pixbuf[key] = gtk.gdk.Pixbuf(
		                          source.get_colorspace(),
		                          source.get_has_alpha(),
		                          source.get_bits_per_sample(),
		                          CARD_WIDTH, CARD_HEIGHT)
		source.copy_area(x*CARD_WIDTH, y*CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT, self.card_pixbuf[key], 0, 0)

	def __initializeCairo(self):

		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 20, 30)
		ctx     = cairo.Context(surface)
		ctx.set_line_width(1)
		ctx.set_source_rgb(0.95, 0.95, 0.95)
		ctx.move_to(10,0)
		ctx.line_to(19,14)
		ctx.stroke()
		ctx.move_to(0,15)
		ctx.line_to(9,29)
		ctx.stroke()

		self.__diagonal_lines_surface_pattern = cairo.SurfacePattern(surface)
		self.__diagonal_lines_surface_pattern.set_extend(cairo.EXTEND_REPEAT)

	###################
	# Signal handlers #
	###################
	def expose(self, widget, event):
		print "Exposing!"
		self.context = widget.window.cairo_create()
		self.context.rectangle(event.area.x, event.area.y,
		                       event.area.width, event.area.height)
		self.context.clip()
		self.draw(self.context)

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



	##############################
	# High-level drawing methods #
	##############################
	def draw(self, context):
		rect = self.get_allocation()

		# The green backgroung doesn't change
		context.rectangle(0, 0, rect.width, rect.height)
		context.set_source_rgb(0.0, 0.8, 0.0)
		context.fill()

		# Draw the different sets of cards
		if self.game_round:
			self.__draw_well_and_stack()
			self.__draw_local_player()
			self.__draw_other_players()

	def __draw_well_and_stack(self):

		print "Drawing well and stack"
		# Save the current source, so we reset it afterwards
		source = self.context.get_source()

		# Draw the area
		x, y = self.coordinates['swa']
		round_rectangle(self.context, x, y, AREAS_LONGSIDE, CARD_HEIGHT + STACK_AREA_VERT_PADDING*2)
		self.context.set_source(self.__diagonal_lines_surface_pattern)
		self.context.fill_preserve()
		self.context.set_source_rgb(0,0,0)
		self.context.stroke()
		self.context.set_source(source)

		# Draw the stack and the well
		x, y = self.coordinates['w']
		self.__draw_card(self.game_round.peek_well_card(), x, y)
		x, y = self.coordinates['s']
		self.__draw_card('reverse', x, y)

	def __draw_local_player(self):
		print "Drawing local player cards"
		x, y = self.coordinates[(0,'c')]
		self.__draw_hand(self.game_round.hands[0], x, y)
		x, y = self.coordinates[(0,'l')]
		self.__draw_lowering_area(x, y)

	def __draw_other_players(self):

		print "Drawing other players cards"
		if self.nr_players == 2:
			x, y = self.coordinates[(1,'c')]
			self.__draw_hand(self.game_round.hands[1], x, y, showRealCards=False)
			x, y = self.coordinates[(1,'l')]
			self.__draw_lowering_area(x, y)
		elif self.nr_players == 3:
			self.__draw_hand(self.game_round.hands[1], 0, 20, showRealCards=False,   orientation=gtk.gdk.PIXBUF_ROTATE_CLOCKWISE)
			self.__draw_hand(self.game_round.hands[2], 200, 20, showRealCards=False, orientation=gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE)
		elif self.nr_players == 4:
			self.__draw_hand(self.game_round.hands[1], 100, 0, showRealCards=False)
			self.__draw_hand(self.game_round.hands[1], 0, 20, showRealCards=False,   orientation=gtk.gdk.PIXBUF_ROTATE_CLOCKWISE)
			self.__draw_hand(self.game_round.hands[2], 200, 20, showRealCards=False, orientation=gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE)

	def __draw_hand(self, cards, x, y, orientation=None, showRealCards=True):
		'''
		Draws a set of cards (a hand) into the area that starts at coordinates (x,y)
		The area measures CARD_HEIGHT in the short-side, and AREAS_LONGSIDE in the long-side.
		Cards are then distributed uniformily across the area.
		'''

		n = len(cards)
		if n != 1:
			delta = (AREAS_LONGSIDE - CARD_WIDTH)/float(n - 1);
		else:
			delta = 0

		if orientation == None:
			for i, card in enumerate(cards):
				if showRealCards:
					self.__draw_card(card, int(x + delta*i), y)
				else:
					self.__draw_card('reverse', int(x + delta*i), y)

		elif orientation == gtk.gdk.PIXBUF_ROTATE_UPSIDEDOWN:
			for i, card in enumerate(cards):
				if showRealCards:
					self.__draw_card(card, int(x + delta*i), y)
				else:
					self.__draw_card('reverse-ud', int(x + delta*i), y)

		elif orientation == gtk.gdk.PIXBUF_ROTATE_CLOCKWISE:
			for i, card in enumerate(cards):
				if showRealCards:
					self.__draw_card(card, x, int(y + delta*i), 'v')
				else:
					self.__draw_card('reverse-cw', x, int(y + delta*i), 'v')

		elif orientation == gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE:
			for i, card in enumerate(cards):
				if showRealCards:
					self.__draw_card(card, x, int(y + delta*i), 'v')
				else:
					self.__draw_card('reverse-ccw', x, int(y + delta*i), 'v')

	#############################
	# Low-level drawing methods #
	#############################
	def __draw_lowering_area(self, x, y, orientation='h'):
		'''
		Draws the lowering area border, in the given coordinates, and with the given dimensions.
		The lowering area is a rounded rectangle with dashed grey border, where the lowered
		card sets are shown. Each player has its own lowering area
		'''

		# Prepare the border style, save old styles
		dash_offset    = self.context.get_dash()
		line_width     = self.context.get_line_width()
		source_pattern = self.context.get_source()

		self.context.set_dash([5])
		self.context.set_line_width(1)
		self.context.set_source_rgb(0.9,0.9,0.9)

		# Draw it!
		if orientation == 'h':
			width, height = (AREAS_LONGSIDE, CARD_HEIGHT)
		else:
			width, hright = (CARD_HEIGHT, AREAS_LONGSIDE)
		round_rectangle(self.context, x, y, width, height)
		self.context.stroke();

		# Reset the context to its previous values
		self.context.set_dash(dash_offset[0], dash_offset[1])
		self.context.set_line_width(line_width)
		self.context.set_source(source_pattern)


	def __draw_card(self, card, x, y, orientation='h'):
		'''
		Draws the given card in the given position. If no orientation parameter is given,
		the card has its natural orientation; otherwise, it is shown oriented depending
		on the value of orientation
		'''
		if orientation == 'h':
			self.window.draw_pixbuf(None, self.card_pixbuf[card], 0, 0, x, y, CARD_WIDTH, CARD_HEIGHT)
		else:
			self.window.draw_pixbuf(None, self.card_pixbuf[card], 0, 0, x, y, CARD_HEIGHT, CARD_WIDTH)

	##########
	# Others #
	##########
	def set_game_round(self, game_round):
		self.game_round = game_round
		self.queue_draw()

	def set_nr_players(self, nr_players):
		self.nr_players = nr_players
		self.__update_player_coordinates();

	def __update_player_coordinates(self):
		'''
		Update the origin coordinates for each player's cards and lowering areas,
		depending on the amount of players for this game.
		'''
		self.coordinates = dict()

		if self.nr_players == 2:
			# Second player goes up
			self.coordinates[(1,'c')] = Coordinates(LEFT_RIGHT_PADDING, TOP_BOTTOM_PADDING)
			self.coordinates[(1,'l')] = Coordinates(LEFT_RIGHT_PADDING, TOP_BOTTOM_PADDING + CARD_HEIGHT + INTER_AREAS_PADDING)
			# Then the well and the stack
			self.coordinates['swa'] = Coordinates(LEFT_RIGHT_PADDING, TOP_BOTTOM_PADDING + CARD_HEIGHT*2 + INTER_AREAS_PADDING*2)
			self.coordinates['s']   = Coordinates(LEFT_RIGHT_PADDING + AREAS_LONGSIDE - (CARD_WIDTH + STACK_AREA_HORIZ_PADDING), TOP_BOTTOM_PADDING + CARD_HEIGHT*2 + INTER_AREAS_PADDING*2 + STACK_AREA_VERT_PADDING)
			self.coordinates['w']   = Coordinates(LEFT_RIGHT_PADDING + AREAS_LONGSIDE - (CARD_WIDTH*2 + STACK_AREA_HORIZ_PADDING + STACK_WELL_SEPARATION), TOP_BOTTOM_PADDING + CARD_HEIGHT*2 + INTER_AREAS_PADDING*2 + STACK_AREA_VERT_PADDING)
			# First player on the bottom
			self.coordinates[(0,'l')] = Coordinates(LEFT_RIGHT_PADDING, TOP_BOTTOM_PADDING + CARD_HEIGHT*3 + INTER_AREAS_PADDING*3 + STACK_AREA_VERT_PADDING*2)
			self.coordinates[(0,'c')] = Coordinates(LEFT_RIGHT_PADDING, TOP_BOTTOM_PADDING + CARD_HEIGHT*4 + INTER_AREAS_PADDING*4 + STACK_AREA_VERT_PADDING*2)
