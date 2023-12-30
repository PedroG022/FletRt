from flet import Page, View
from flet import RouteChangeEvent, TemplateRoute

from fletrt import Route, NavigationRoute
from fletrt.templates import NotFound
from fletrt.utils import get_navigation_destinations


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

        self.__parent_routes: dict = {}

    # Sets the router to intercept the page changes
    def install(self):
        self.__page.on_route_change = self.__on_route_change
        self.__page.go(self.__page.route)

    # Initialize the route essential variables
    def __initialize_route(self, route: Route, route_path: str, route_params: dict = None):
        route.page = self.__page
        route.path = route_path

        route.route_params = route_params

        route.pop = self.__route_pop
        route.go = self.__route_go

        # Checks if the route have sub-routes, for cases like
        # the NavigationRoute, where the parent view must be rendered
        # before the subpages are rendered
        if isinstance(route, NavigationRoute):
            dependant = get_navigation_destinations(route.path, route.navigation_bar)

            for dependant_route in dependant:
                self.__parent_routes[dependant_route] = route.path

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

    # Gets the matching template for an url
    def __template_from_path(self, route_path: str):
        template_route = TemplateRoute(route_path)

        for template_route_path in self.__route_paths:
            if template_route.match(template_route_path) and ':' in template_route_path:
                return template_route_path

        return None

    # Gets the parameters that are included in a route path
    def __route_params(self, route_path: str) -> dict:
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

    # Returns the route template path and
    # the route params, if the route contains params.
    def __get_route(self) -> (str, dict):
        route_path = self.__page.route

        params = None

        if self.__route_match_template(self.__page.route):
            route_path = self.__template_from_path(self.__page.route)
            params = self.__route_params(self.__page.route)

        if route_path not in self.__route_paths:
            return None, None

        return route_path, params

    # Presents the target route by pushing the route's
    # view to the page views list
    def __present_route(self, target_route: Route):
        self.__page.views.clear()

        target_route_view: View = target_route.view()
        target_route.route_data = None

        self.__page.views.append(target_route_view)
        self.__page.update()

    # Change the current page's body to the current route's body
    def __present_body(self, target_route: Route):
        # TODO: Find a way to pass the view arguments to the view, or pass the navigation bar to the page instead of the view
        target_view: View = self.__page.views[-1]

        self.__copy_properties(target_route.view(), target_view)

        target_view.controls = target_route.view().controls
        self.__page.update()

        target_route.route_data = None

    def __present_navigation_route(self, target_route: Route):
        target_route_path = target_route.path

        root_route_path = self.__parent_routes[target_route_path]
        root_route: NavigationRoute = self.__routes_dict.get(root_route_path)

        self.__present_route(root_route)

        self.__page.views[-1].controls = [target_route.body()]

        # Gets the navigation bar target index
        dependant = get_navigation_destinations(root_route.path, root_route.navigation_bar)
        index = dependant.index(target_route_path)

        self.__page.views[-1].navigation_bar.selected_index = index
        self.__page.update()

        target_route.route_data = None

    def __copy_properties(self, source: View, target: View):
        target.vertical_alignment = source.vertical_alignment
        target.horizontal_alignment = source.horizontal_alignment
        target.padding = source.padding
        target.auto_scroll = source.auto_scroll
        target.bgcolor = source.bgcolor

    # Wrapper for the route change event, that allows passing data to the target page
    def __on_route_change(self, route_change_event: RouteChangeEvent):
        target_route_path, target_route_params = self.__get_route()

        if not target_route_path:
            self.__page.go('/404')
            return

        target_route: Route = self.__routes_dict.get(target_route_path)

        if not target_route.initialized:
            self.__initialize_route(target_route, target_route_path, target_route_params)

        # Checks whether the target route is a children of a NavigationRoute.
        # If not, it will render the page normally
        if target_route_path not in self.__parent_routes.keys():
            self.__present_route(target_route)
            return

        # Check if the root navigation route was already rendered. If it is,
        # just the body contents will be updated.
        if target_route.route_data and target_route.route_data.get('keep'):
            self.__present_body(target_route)
            return

        # Renders the NavigationRoute
        self.__present_navigation_route(target_route)

    def __past_routes(self):
        return [f'/{path}' for path in self.__page.route.split('/')]
