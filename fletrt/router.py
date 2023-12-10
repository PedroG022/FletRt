from flet import Page, View
from flet import RouteChangeEvent, TemplateRoute

from fletrt import Route
from fletrt.templates import NotFound


class Router:

    # Initialize the router
    def __init__(self, page: Page, routes: dict, starting_route: str = '/'):
        self.page: Page = page

        # Intercepts not found pages
        routes['/404'] = NotFound()

        # Sets variables that will be used
        self.routes_dict: dict = routes
        self.route_paths = [path for path in self.routes_dict.keys()]
        self.starting_route: str = starting_route

    # Sets the router to intercept the page changes
    def install(self):
        self.page.on_route_change = self.on_route_change
        self.page.route = self.starting_route
        self.page.go(self.page.route)

    # Initialize the route essential variables
    def initialize_route(self, route: Route, path: str):
        if not route.initialized:
            route.page = self.page
            route.path = path

            route.pop = self.route_pop
            route.go = self.route_go

            route.initialized = True

    # Alternative to the page.views.pop function
    def route_pop(self):
        last_route = self.past_routes()[-2]
        self.page.go(last_route)

    # Wrapper for the page.go function
    def route_go(self, route):
        self.page.go(route)

    def on_route_change(self, route_change_event: RouteChangeEvent):
        self.page.views.clear()

        template_route = TemplateRoute(self.page.route)

        target_route_path = route_change_event.route
        target_route_params = None

        for template_route_path in self.route_paths:
            if template_route.match(template_route_path) and ':' in template_route_path:
                template_route_components: list = template_route_path.split('/')
                route_path_components = [component for component in self.page.route.split('/')]

                templates = {
                    template_name[1:]: template_route_components.index(template_name)
                    for template_name in template_route_components
                    if template_name.startswith(':')
                }

                route_params = {template_name: route_path_components[templates[template_name]]
                                for template_name in templates.keys()}

                target_route_path = template_route_path
                target_route_params = route_params

        if not self.validate_route(target_route_path):
            return

        target_route: Route = self.routes_dict.get(target_route_path)
        self.initialize_route(target_route, target_route_path)

        target_route.route_params = target_route_params

        target_route_view: View = target_route.view()

        self.page.views.append(target_route_view)
        self.page.update()

    # Checks if the route that's being navigated to
    # exists. If not, return a 404 Not Found page.
    def validate_route(self, route=None):
        if route not in self.route_paths:
            self.page.go('/404')
            return False
        return True

    def past_routes(self):
        return [f'/{path}' for path in self.page.route.split('/')]

    def debug(self):
        print('> Debug')
        print(f'\troutesPath: {self.route_paths}')
        print(f'\troutesDict: {self.routes_dict}')
        print(f'\tstartingRoute: {self.starting_route}')
