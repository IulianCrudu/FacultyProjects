from src.settings import Settings
from src.ui import UI

settings = Settings()
ui = UI(dimension=settings.dim, apple_count=settings.apple_count)
ui.start()
