# baydemir: Comments in this file are not especially great.

import wx

############################################################################
# Tic-tac-toe game (backend).

class TicTacToeBackend(object):
    """
    A simple class to manage a tic-tac-toe board.
    """

    PLAYER_X = 'x'
    PLAYER_O = 'o'

    def __init__(self):
        self.board = [[None for i in range(0, 3)] for j in range(0, 3)]
        self.turn = TicTacToeBackend.PLAYER_X

    def new_game(self):
        """
        Resets the board to be completely blank.
        """

        for i in range(0, 3):
            for j in range(0, 3):
                self.board[i][j] = None

    def is_game_over(self):
        """
        Returns either PLAYER_X or PLAYER_O, if one of them has one,
        and False otherwise.
        """

        # This is an ugly way to code this check...

        if self.board[0][0] == self.board[0][1] == self.board[0][2]:
            return self.board[0][0]
        if self.board[1][0] == self.board[1][1] == self.board[1][2]:
            return self.board[1][0]
        if self.board[2][0] == self.board[2][1] == self.board[2][2]:
            return self.board[2][0]

        if self.board[0][0] == self.board[1][0] == self.board[2][0]:
            return self.board[0][0]
        if self.board[0][1] == self.board[1][1] == self.board[2][1]:
            return self.board[0][1]
        if self.board[0][2] == self.board[1][2] == self.board[2][2]:
            return self.board[0][2]

        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[2][0] == self.board[1][1] == self.board[0][2]:
            return self.board[2][0]

        occupied = True
        for i in range(0, 3):
            for j in range(0, 3):
                occupied = occupied and self.board[i][j]

        return occupied

    def current_turn(self):
        """
        Returns PLAYER_X or PLAYER_O, depending on whose turn
        it currently is.
        """

        return self.turn

    def make_move(self, i, j):
        """
        Sets location (i, j) in the board to player.
        Returns False if the move is illegal, and True otherwise.
        """

        assert (0 <= i < 3 and 0 <= j < 3)

        if self.board[i][j] != None or self.is_game_over():
            return False

        self.board[i][j] = self.turn
        if self.turn == TicTacToeBackend.PLAYER_X:
            self.turn = TicTacToeBackend.PLAYER_O
        else:
            self.turn = TicTacToeBackend.PLAYER_X

        return True

    def get_pos(self, i, j):
        """
        Returns location (i, j) of the board.  It will be one of
        PLAYER_X, PLAYER_O, or None.
        """

        return self.board[i][j]

############################################################################
# Tic-tac-toe main frame.

class TicTacToeFrame(wx.Frame):
    def __init__(self, *args, **keywords):
        """
        Constructor; arguments are exactly as they would be for wx.Frame.
        """

        wx.Frame.__init__(self, *args, **keywords)
        self.Create()

    def Create(self):
        """
        Does most of the work in creating the UI elements of this frame.
        Initializes the backend, if necessary.
        """

        try:
            if self.backend == None: pass
        except AttributeError:
            self.InitBackend()

        self.CreateMenus()
        self.CreateStatusBar()
        self.CreateMainArea()

    def CreateMenus(self):
        """
        Create the menus for this frame.
        """

        bar = wx.MenuBar()

        menu = wx.Menu()
        newItem = wx.MenuItem(menu, wx.ID_ANY, '&New game', help='Create a new game')
        quitItem = wx.MenuItem(menu, wx.ID_ANY, '&Quit', help='Quit this program')

        menu.AppendItem(newItem)
        menu.AppendItem(quitItem)

        bar.Append(menu, '&Main')
        self.SetMenuBar(bar)

        # I think only Menu related classes don't have a Bind method.

        self.Bind(wx.EVT_MENU, self.Quit, source=quitItem)
        self.Bind(wx.EVT_MENU, self.NewGame, source=newItem)

    def CreateStatusBar(self):
        """
        Creates the status bar for this frame.
        """

        self.status = wx.StatusBar(self, wx.ID_ANY)
        self.SetStatusBar(self.status)
        self.status.SetFields(['Welcome to Tic-Tac-Toe!'])

    def CreateMainArea(self):
        """
        Creates the main button panel for this frame.
        Sets the sizer for this frame, in the process.
        """

        gs = wx.GridSizer(3, 3, 0, 0)

        # Bad idea to hard code paths here.
        # Arguably also a bad idea to add things to the frame directly.

        self.img_blank = wx.Bitmap('blank.png', wx.BITMAP_TYPE_PNG)
        self.img_x = wx.Bitmap('x.png', wx.BITMAP_TYPE_PNG)
        self.img_o = wx.Bitmap('o.png', wx.BITMAP_TYPE_PNG)

        self.buttons = [[wx.BitmapButton(self, j*3 + i, self.img_blank)
                                         # size=(200, 200),
                                         # pos=(100, 100)
                                         # ) \
                        for i in range(0, 3)] \
                        for j in range(0, 3)]

        for i in range(0, 3):
            for j in range(0, 3):
                gs.Add(self.buttons[i][j], 0, flag=wx.EXPAND)
                self.Bind(wx.EVT_BUTTON, self.HandleButton, source=self.buttons[i][j])

        self.SetSizerAndFit(gs)

    def HandleCheck(self, event):
        print "Check box checked!"
        print self.box.GetValue()

    def InitBackend(self):
        """
        Initializes the backend.
        """

        self.backend = TicTacToeBackend()
        self.initialized = True
        self.X = TicTacToeBackend.PLAYER_X
        self.O = TicTacToeBackend.PLAYER_O

    def HandleButton(self, event):
        """
        Handle a button press.
        """

        id = event.GetId()
        i, j = id / 3, id % 3
        result = self.backend.make_move(i, j)

        def string_of_turn():
            if self.backend.current_turn() == self.X:
                return "X's turn."
            else:
                return "O's turn."

        if not result :
            self.status.SetFields(['Illegal move. ' + string_of_turn()])
        else:
            self.status.SetFields([string_of_turn()])
        if self.backend.is_game_over() :
            self.status.SetFields(['Game over!'])

        self.UpdateButtons()

    def UpdateButtons(self):
        """
        Update the bitmaps on the buttons.
        """

        for i in range(0, 3):
           for j in range(0, 3):
               if self.backend.get_pos(i, j) == self.X:
                   self.buttons[i][j].SetBitmapLabel(self.img_x)
               elif self.backend.get_pos(i, j) == self.O:
                   self.buttons[i][j].SetBitmapLabel(self.img_o)
               else:
                   self.buttons[i][j].SetBitmapLabel(self.img_blank)
               self.buttons[i][j].Refresh()

    def NewGame(self, event):
        """
        Event handler: Starts a new game.
        """

        self.backend.new_game()
        self.UpdateButtons()

    def Quit(self, event):
        """
        Event handler: 'Quits' this program by destroying this frame.
        """

        self.Destroy()

############################################################################
# Main loop.  (Almost just boilerplate.)

def main():
    """
    Runs a tic-tac-toe game.
    """

    app = wx.App(redirect = False)
    frame = TicTacToeFrame(None, wx.ID_ANY, title='Tic Tac Toe for 2 players')
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()
