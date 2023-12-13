from flet import Page, View
from flet import RouteChangeEvent, TemplateRoute

from fletrt import Route
from fletrt.templates import NotFound


class Router:

    # Initialize the router
    def __init__(self, page: Page, routes: dict, starting_route: str = '/'):
        self.__page: Page = page

        # Intercepts not found pages
        routes['/404'] = NotFound()

        # Sets variables that will be used
        self.__routes_dict: dict = routes
        self.__route_paths = [path for path in self.__routes_dict.keys()]
        self.__starting_route: str = starting_route

    # Sets the router to intercept the page changes
    def install(self):
        self.__page.on_route_change = self.__on_route_change
        self.__page.route = self.__starting_route
        self.__page.go(self.__page.route)

    # Initialize the route essential variables
    def __initialize_route(self, route: Route, route_path: str):
        route.page = self.__page
        route.path = route_path

        route.pop = self.__route_pop
        route.go = self.__route_go

        route.initialized = True

    # Alternative to the page.views.pop function
    def __route_pop(self):
        last_route = self.__past_routes()[-2]
        self.__page.go(last_route)

    # Wrapper for the page.go function
    def __route_go(self, route_path: str, route_data: dict = None):
        template_path = route_path

        if self.__route_match_template(route_path):
            template_path = self.__template_from_path(route_path)

        target_route: Route = self.__routes_dict[template_path]
        target_route.route_data = route_data
        self.__routes_dict[route_path] = target_route

        self.__page.go(route_path)

    def __route_match_template(self, route_path: str) -> bool:
        template_route = TemplateRoute(route_path)

        for template in [key for key in self.__routes_dict.keys() if ':' in key]:
            if template_route.match(template):
                return True

        return False

    # Gets the matching path for an url, even
    # if is a template (e.g: /users/:id)
    def __template_from_path(self, route_path: str):
        template_route = TemplateRoute(route_path)

        for template_route_path in self.__route_paths:
            if template_route.match(template_route_path) and ':' in template_route_path:
                return template_route_path

        return None

    def __route_params(self, route_path: str):
        path_template = self.__template_from_path(route_path)

        if path_template:
            template_route_components: list = path_template.split('/')
            route_path_components = [component for component in self.__page.route.split('/')]

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

    def __get_route(self):
        route_path = self.__page.route

        params = None

        if self.__route_match_template(self.__page.route):
            route_path = self.__template_from_path(self.__page.route)
            params = self.__route_params(self.__page.route)

        if route_path not in self.__route_paths:
            self.__page.go('/404')
            return None, None

        return route_path, params

    # Wrapper for the route change event, that allows passing data
    # to the target page
    def __on_route_change(self, route_change_event: RouteChangeEvent):
        self.__page.views.clear()

        target_route_path, target_route_params = self.__get_route()

        if target_route_path:
            target_route: Route = self.__routes_dict.get(target_route_path)

            if not target_route.initialized:
                self.__initialize_route(target_route, target_route_path)

            target_route.route_params = target_route_params

            target_route_view: View = target_route.view()
            target_route.route_data = None

            self.__page.views.append(target_route_view)
            self.__page.update()

    def __past_routes(self):
        return [f'/{path}' for path in self.__page.route.split('/')]
