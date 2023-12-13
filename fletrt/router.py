from flet import Page, View
from flet import RouteChangeEvent, TemplateRoute

from fletrt import Route
from fletrt.templates import NotFound

import inspect


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
    def route_go(self, target_route_path, target_route_data: dict = None):
        print('route_go', target_route_path, target_route_data)

        template_route = self.template_from_path(target_route_path)

        if template_route:
            target_route: Route = self.routes_dict[template_route]
            target_route.route_data = target_route_data

            self.routes_dict[target_route_path] = target_route

        self.page.go(target_route_path)

    # Gets the matching path for an url, even
    # if is a template (e.g: /users/:id)
    def template_from_path(self, route_path: str):
        cal = inspect.getouterframes(inspect.currentframe(), 2)[1][3]
        print('template_from_path', route_path, cal)

        template_route = TemplateRoute(route_path)

        for template_route_path in self.route_paths:
            if template_route.match(template_route_path) and ':' in template_route_path:
                return template_route_path

        return None

    def route_params(self, route_path: str):
        print('route_params')

        path_template = self.template_from_path(route_path)

        if path_template:
            template_route_components: list = path_template.split('/')
            route_path_components = [component for component in self.page.route.split('/')]

            templates = {
                template_name[1:]: template_route_components.index(template_name)
                for template_name in template_route_components
                if template_name.startswith(':')
            }

            return {
                template_name: route_path_components[templates[template_name]]
                for template_name in templates.keys()
            }

        return None

    def get_route(self):
        path = self.page.route
        template_path = self.template_from_path(self.page.route)

        params = None

        if template_path:
            path = template_path
            params = self.route_params(self.page.route)

        if path not in self.route_paths:
            self.page.go('/404')
            return None, None

        return path, params

    # Wrapper for the route change event, that allows passing data
    # to the target page
    def on_route_change(self, route_change_event: RouteChangeEvent):
        self.page.views.clear()

        target_route_path, target_route_params = self.get_route()

        if target_route_path:
            target_route: Route = self.routes_dict.get(target_route_path)

            if not target_route.initialized:
                self.initialize_route(target_route, target_route_path)

            target_route.route_params = target_route_params

            target_route_view: View = target_route.view()
            target_route.route_data = None

            self.page.views.append(target_route_view)
            self.page.update()

    def past_routes(self):
        return [f'/{path}' for path in self.page.route.split('/')]
