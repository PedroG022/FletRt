from typing import Optional

from flet import Page, View
from flet import RouteChangeEvent, TemplateRoute

from fletrt.utils import get_navigation_destinations
from .navigation_route import NavigationRoute
from .route import Route
from .routing_middleware import RoutingMiddleware
from .templates.not_found import NotFound


class Router:

    # Initialize the router
    def __init__(self,
                 page: Page,
                 routes: dict,
                 not_found_route: Route = NotFound(),
                 redirect_not_found: bool = True,
                 routing_middleware: type[RoutingMiddleware] = None):

        # Initialize the router's variables
        self.__page: Page = page
        self.__redirect_not_found = redirect_not_found
        self.__current_route = self.__page.route
        self.__routing_middleware: Optional[RoutingMiddleware] = None

        # If available, instantiate the routing middleware
        if routing_middleware:
            self.__routing_middleware: RoutingMiddleware = routing_middleware(self.__page)

        # Intercepts not found pages
        routes['/404'] = not_found_route

        # Sets variables that will be used
        self.__routes_dict: dict = routes
        self.__route_paths = [path for path in self.__routes_dict.keys()]

        self.__parent_routes: dict = {}
        self.__initialize_routes()

    # Sets the router to intercept the page changes
    def install(self):
        self.__page.on_route_change = self.__on_route_change
        self.__page.go(self.__page.route)

    def __initialize_routes(self):
        for route_path in self.__routes_dict.keys():
            route = self.__routes_dict[route_path]

            route.page = self.__page
            route.path = route_path

            route.pop = self.__route_pop
            route.go = self.__route_go

            # Checks if the route have sub-routes, for cases like
            # the NavigationRoute, where the parent view must be rendered
            # before the subpages are rendered
            if isinstance(route, NavigationRoute):
                dependant = route.destinations

                if not dependant:
                    dependant = get_navigation_destinations(route.path, route.navigation_bar)

                for dependant_route in dependant:
                    self.__parent_routes[dependant_route] = route.path

    # Alternative to the page.views.pop function
    def __route_pop(self):
        path_components = [item for item in self.__past_routes()[:-1] if item != '/']
        path = ''.join(path_components)

        if path == '':
            path = '/'

        self.__page.go(path)

    # Wrapper for the page.go function
    def __route_go(self, route_path: str):
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
    def __route_params(self, route_path: str) -> Optional[dict]:
        path_template = self.__template_from_path(route_path)

        if path_template:
            template_route_components: list = path_template.split('/')
            route_path_components = [component for component in route_path.split('/')]

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
    def __get_route(self, route_path: str) -> (str, dict):
        params = None

        # Verify if an exact match is available, ignoring params
        if route_path in self.__route_paths:
            return route_path, params

        if self.__route_match_template(route_path):
            route_path_copy = route_path
            route_path = self.__template_from_path(route_path_copy)
            params = self.__route_params(route_path_copy)

        if route_path not in self.__route_paths:
            return None, None

        return route_path, params

    # Presents the target route by pushing the route's
    # view to the page views list
    def __present_route(self, target_route: Route):
        self.__page.views.clear()

        target_route_view: View = target_route.view()

        self.__page.views.append(target_route_view)
        self.__page.update()

    def __present_navigation_route(self, target_route: Route):
        target_route_path = target_route.path

        root_route_path = self.__parent_routes[target_route_path]
        root_route: NavigationRoute = self.__routes_dict.get(root_route_path)

        self.__present_route(root_route)

        self.__page.views[-1].controls = [target_route.body()]
        self.__copy_properties(target_route.view(), self.__page.views[-1])

        # Gets the navigation bar target index
        dependant = root_route.destinations
        index = dependant.index(target_route_path)

        self.__page.views[-1].navigation_bar.selected_index = index
        self.__page.update()

    # Copies properties from one view to another
    @staticmethod
    def __copy_properties(source: View, target: View):
        target.vertical_alignment = source.vertical_alignment
        target.horizontal_alignment = source.horizontal_alignment
        target.padding = source.padding
        target.auto_scroll = source.auto_scroll
        target.bgcolor = source.bgcolor
        target.floating_action_button = source.floating_action_button

    # Wrapper for the route change event
    def __on_route_change(self, route_change_event: RouteChangeEvent):

        # Verify if a RoutingMiddleware is available, and if it is,
        # it gets executed before any logic. If the method before_route_change
        # returns false, then no logic will be executed at all.
        if self.__routing_middleware:
            self.__routing_middleware.source_route = self.__current_route
            result = self.__routing_middleware.before_route_change(self.__current_route, route_change_event.route)

            if not result:
                return

        self.__current_route = self.__page.route

        # Verify the existence of the target route and also get possible parameters
        target_route_path, target_route_params = self.__get_route(route_change_event.route)

        # If it does not exist, the 404 route will either be redirected to or 'presented'
        if not target_route_path:
            if self.__redirect_not_found:
                self.__page.go('/404')
            else:
                self.__present_route(self.__routes_dict['/404'])
            return

        # Get the route object from the dict
        target_route: Route = self.__routes_dict.get(target_route_path)

        # Checks if the target route has been initialized.
        target_route.route_params = target_route_params

        # Checks whether the target route is a navigation root
        # if it is, it will render the first page
        if target_route_path in self.__parent_routes.values():
            target_route: NavigationRoute

            destinations = target_route.destinations
            first_route = destinations[0]

            self.__page.go(first_route)
            return

        # Checks whether the target route is a children of a NavigationRoute.
        # If not, it will render the page normally
        if target_route_path not in self.__parent_routes.keys():
            self.__present_route(target_route)
            return

        # Renders the NavigationRoute
        self.__present_navigation_route(target_route)

    def __past_routes(self):
        return [f'/{path}' for path in self.__page.route.split('/')]
