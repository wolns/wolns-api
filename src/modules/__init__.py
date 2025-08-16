from src.modules.singers import controllers as singers_controllers
from src.modules.tracks import controllers as tracks_controllers
from src.modules.users import controllers as users_controllers

controllers = (*users_controllers, *singers_controllers, *tracks_controllers)
