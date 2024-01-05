import flet as ft

from page_index import Index
from page_home import Home
from page_settings import Settings
from page_content import Content

from fletrt import Router


def main(page: ft.Page):
    router = Router(page=page, routes={
        '/': Index(),
        '/home': Home(),
        '/home/:content': Content(),
        '/settings': Settings(),
    }, redirect_not_found=False)

    router.install()


ft.app(target=main, view=ft.WEB_BROWSER, port=40445)
