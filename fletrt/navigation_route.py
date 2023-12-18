from flet_core import View

from fletrt import Route

from flet import NavigationBar, NavigationDrawer, FloatingActionButton, AppBar, ControlEvent

from fletrt.utils import get_navigation_destinations


class NavigationRoute(Route):
    def __init__(self):
        super().__init__()

        self.navigation_bar = self.navigation_bar()

    def navigation_bar(self) -> (NavigationBar, list):
        pass

    def drawer(self) -> NavigationDrawer:
        pass

    def end_drawer(self) -> NavigationDrawer:
        pass

    def floating_action_button(self) -> FloatingActionButton:
        pass

    def app_bar(self) -> AppBar:
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
        base.floating_action_button = self.floating_action_button()
        base.appbar = self.app_bar()
        base.drawer = self.drawer()
        base.end_drawer = self.end_drawer()

        return base
