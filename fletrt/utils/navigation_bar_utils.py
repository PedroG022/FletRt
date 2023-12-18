from flet import NavigationBar


def get_navigation_destinations(path: str, navigation_bar: NavigationBar) -> list:
    return [f'{path}/{destination.label.lower()}'
            if path != '/' else f'/{destination.label.lower()}'
            for destination in navigation_bar.destinations]
