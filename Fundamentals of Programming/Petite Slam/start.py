from src.ui.menu_ui import UI
from src.service.player_service import PlayerService
from src.repository import FileRepository

player_repo = FileRepository("players.txt")
player_service = PlayerService(repo=player_repo)
ui = UI(player_service=player_service)
ui.start()
