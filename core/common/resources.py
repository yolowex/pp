from core.common.names import *
from core.event_holder import EventHolder

screen: Optional[Surface] = None
event_holder: Optional[EventHolder] = None

def sc_center() -> Vector2:
    return Vector2(screen.get_rect().center)