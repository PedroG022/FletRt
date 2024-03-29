from flet import NavigationBar, ControlEvent, View

from fletrt import Route
from fletrt.utils import get_navigation_destinations

from typing import Optional


class NavigationRoute(Route):
    def __init__(self):
        super().__init__()

        self.navigation_bar: NavigationBar = self.navigation_bar()
        self.destinations: Optional[list] = None

    def navigation_bar(self) -> NavigationBar:
        pass

    def on_navigation_bar_change(self, event: ControlEvent, destinations: list):
        route_path = destinations[int(event.data)]
        self.go(route_path)

    def view(self) -> View:
        base = super().view()

        navigation_bar = self.navigation_bar

        if navigation_bar:
            if not self.destinations:
                self.destinations = get_navigation_destinations(self.path, navigation_bar)

            navigation_bar.on_change = lambda e: self.on_navigation_bar_change(e, self.destinations)

        base.navigation_bar = navigation_bar

        return base
