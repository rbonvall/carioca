#!/usr/bin/env python

import gtk
import pygtk

from card_area import CardArea
from carioca import CariocaGame

APP_NAME = 'carioca'

def runOKCancelDialog(title, labelText):
	label = gtk.Label(labelText)
	label.show()
	dialog = gtk.Dialog(title=title,
	                    buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT),
	                    flags=gtk.DIALOG_MODAL)
	dialog.set_has_separator(True)
	dialog.vbox.pack_start(label, True, True, 0)
	result = dialog.run()
	dialog.destroy()
	return result


class CariocaGUI:

	def __init__(self):

		# Initial attributes
		self.game = None
		self.gameRound = None

		# The main window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect('delete_event', self.delete_window_handler)
		self.window.connect('destroy', self.destroy_handler)
		self.window.set_title(APP_NAME)

		vbox = gtk.VBox(False, 0)
		vbox.show()

		self.createMenu(vbox)
		self.createDrawingArea(vbox)

		# Finally, show the window
		self.window.add(vbox)
		self.window.show()

	def createMenu(self, vbox):

		menu_items = (
			( "/_File", None, None, 0, "<Branch>" ),
			( "/File/_New game", "<control>N", lambda a,b: self.new_game(), 0, None),
			( "/File/_Quit " + APP_NAME, "<control>Q", self.quit_handler, 0, None),
			( "/_Help", None, None, 0, "<Branch>"),
			( "/Help/_About", None, lambda a,b: self.about(), 0, None),
		)

		accel_group = gtk.AccelGroup()
		self.item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
		self.item_factory.create_items(menu_items)
		self.window.add_accel_group(accel_group)

		vbox.pack_start(self.item_factory.get_widget("<main>"), False, False, 0)


	def createDrawingArea(self, vbox):
		self.drawing_area = CardArea()
		self.drawing_area.set_size_request(500, 500)
		self.drawing_area.show()	

		vbox.pack_start(self.drawing_area, True, True, 0)

	def main(self):
		gtk.main()

	def about(self):
		aboutDialog = gtk.AboutDialog()
		aboutDialog.set_authors([u'Roberto Bonvallet', u'Rodrigo Tobar'])
		aboutDialog.set_name(u'Carioca')
		aboutDialog.show()

	###################
	# Signal handlers #
	###################
	def delete_window_handler(self, widget, event, data=None):

		if self.game == None:
			return False

		# Dialog confirming user exit
		result = runOKCancelDialog("Quit " + APP_NAME, "Are you sure that you want to quit from " + APP_NAME)
		if result == gtk.RESPONSE_OK:
			return False
		else:
			return True

	def destroy_handler(self, widget, data=None):
		gtk.main_quit()

	def quit_handler(self, widget, data=None):
		self.delete_window_handler(self, widget, None)


	##################
	# Game lifecycle #
	##################
	def new_game(self):

		# If there is a current game, check if we want to abandon it
		if( self.game is not None ):
			result = runOKCancelDialog("Abandon game?", "Are you sure that you want to abandon the current game?")
			if result == gtk.RESPONSE_REJECT:
				return

		# Abandon game and start a new one
		self.abandon_game()

		# Number of players
		spinner = gtk.SpinButton(adjustment=gtk.Adjustment(value=2, step_incr=1, lower=2, upper=4))
		spinner.show()
		label   = gtk.Label("How may player will participate?")
		label.show()

		hbox = gtk.HBox(False, 2)
		hbox.pack_start(label)
		hbox.pack_end(spinner)
		hbox.show()

		dialog = gtk.Dialog(title="Players", buttons=("OK", 1, "Cancel", 2), flags=gtk.DIALOG_MODAL)
		dialog.set_has_separator(True)
		dialog.vbox.pack_start(hbox, True, True, 0)
		result = dialog.run()
		dialog.destroy()
		if result == 2:
			return

		num_players = spinner.get_value_as_int()
		print "Starting a new game with %d players" % (num_players)
		self.game = CariocaGame(num_players)

	def abandon_game(self):

		# Don't abandon anything there is nothing to abandon
		if self.game is None:
			return

		print "Abandoning game"
		self.game = None



# If called as program, run the GUI
if __name__ == "__main__":
	gui = CariocaGUI()
	gui.main()
