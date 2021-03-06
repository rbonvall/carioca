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
	                    flags=gtk.DIALOG_MODAL)

	dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK).grab_default()
	dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
	dialog.set_has_separator(True)
	dialog.vbox.pack_start(label, True, True, 0)
	result = dialog.run()
	dialog.destroy()

	if result != gtk.RESPONSE_OK:
		return False
	return True


class CariocaGUI:

	def __init__(self):

		# Initial attributes
		self.game = None
		self.gameRound = None

		# Bulid the GUI and show it
		self.build()


	########################
	# GUI building methods #
	########################
	def build(self):

		# The main window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect('delete_event', self.delete_window_handler)
		self.window.connect('destroy', self.destroy_handler)
		self.window.set_title(APP_NAME)

		# VBox that will contain the main widgets of the window
		vbox = gtk.VBox(False, 0)
		vbox.show()

		self.__createMenu(vbox)
		self.__createDrawingArea(vbox)
		self.__createStatusBar(vbox)

		self.window.add(vbox)
		self.window.show()

	def __createMenu(self, vbox):

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

		main_menu = self.item_factory.get_widget("<main>")
		main_menu.show()
		vbox.pack_start(main_menu, False, False, 0)


	def __createDrawingArea(self, vbox):
		self.drawing_area = CardArea()
		self.drawing_area.set_size_request(500, 500)
		self.drawing_area.show()	

		vbox.pack_start(self.drawing_area, True, True, 0)

	def __createStatusBar(self, vbox):
		self.status_bar = gtk.Statusbar()
		self.status_bar.show()
		vbox.pack_end(self.status_bar, True, False, 0)

	###################
	# Signal handlers #
	###################
	def delete_window_handler(self, widget, event, data=None):
		return not self.confirm_end_carioca()

	def destroy_handler(self, widget, data=None):
		gtk.main_quit()

	def quit_handler(self, widget, data=None):
		if self.confirm_end_carioca():
			self.window.destroy()

	##################
	# Game lifecycle #
	##################
	def new_game(self):

		# If there is a current game, check if we want to abandon it
		if( self.game is not None ):
			result = runOKCancelDialog("Abandon game?", "Are you sure that you want to abandon the current game?")
			if not result:
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

		dialog = gtk.Dialog(title="Players", flags=gtk.DIALOG_MODAL)
		dialog.set_has_separator(True)

		okButton = dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		okButton.grab_default()
		okButton.grab_focus()
		dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		dialog.vbox.pack_start(hbox, True, True, 0)
		result = dialog.run()
		dialog.destroy()
		if result != gtk.RESPONSE_OK:
			return

		num_players = spinner.get_value_as_int()
		self.game = CariocaGame(num_players)

		self.current_round =	self.game.go_to_next_round()

		# Update the GUI with current round
		self.drawing_area.set_nr_players(num_players)
		self.drawing_area.set_game_round(self.current_round)


	def abandon_game(self):

		# Don't abandon anything there is nothing to abandon
		if self.game is None:
			return

		self.game = None


	def confirm_end_carioca(self):
		if self.game == None:
			return True

		# Dialog confirming user exit
		result = runOKCancelDialog("Quit " + APP_NAME, "Are you sure that you want to quit from " + APP_NAME)
		if result:
			self.abandon_game()
		return result

	##########
	# Others #
	##########
	def main(self):
		gtk.main()

	def about(self):
		aboutDialog = gtk.AboutDialog()
		aboutDialog.set_authors([u'Roberto Bonvallet', u'Rodrigo Tobar'])
		aboutDialog.set_name(u'Carioca')
		aboutDialog.set_comments(u'A carioca game written in python')
		aboutDialog.run()
		aboutDialog.destroy()


# If called as program, run the GUI
if __name__ == "__main__":
	gui = CariocaGUI()
	gui.main()
