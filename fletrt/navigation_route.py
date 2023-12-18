from flet_core import View

from fletrt import Route

from flet import NavigationBar, ControlEvent

from fletrt.utils import get_navigation_destinations


class NavigationRoute(Route):
    def __init__(self):
        super().__init__()

        self.navigation_bar = self.navigation_bar()

    def navigation_bar(self) -> (NavigationBar, list):
        pass

    def on_navigation_bar_change(self, event: ControlEvent, destinations: list):
        route_path = destinations[int(event.data)]
        self.go(route_path, {'keep': True})

    def view(self) -> View:
        base = super().view()

        navigation_bar = self.navigation_bar

        if navigation_bar:
            destinations = get_navigation_destinations(self.path, navigation_bar)
            navigation_bar.on_change = lambda e: self.on_navigation_bar_change(e, destinations)

        base.navigation_bar = navigation_bar

        return base
