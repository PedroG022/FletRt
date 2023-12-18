import flet as ft

from page_index import Index
from page_home import Home
from page_settings import Settings

from fletrt import Router


def main(page: ft.Page):
    router = Router(page=page, routes={
        '/': Index(),
        '/home': Home(),
        '/settings': Settings()
    })

    router.install()


ft.app(target=main, view=ft.WEB_BROWSER, port=40444)
