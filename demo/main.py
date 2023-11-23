import flet as ft
from fletrt import Router

from page_a import PageA
from page_b import PageB


def main(page: ft.Page):
    Router(page, routes={
        '/page-a': PageA(),
        '/page-b': PageB()
    }, starting_route='/page-a')


ft.app(target=main)
