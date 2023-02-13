# --------------- BIPOLE III ----------------------
# Run this file to play Bipole III.
# infinityjka.itch.io

import os

#Comment this out and make sure to run from this file's folder if the game doesn't work
os.chdir( os.path.dirname( os.path.abspath(__file__) ) )

from lib import main
main.mainloop()