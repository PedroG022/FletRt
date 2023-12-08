import flet as ft

from page_a import PageA
from page_b import PageB
from page_c import PageC

from fletrt import Router


def main(page: ft.Page):
    router = Router(page=page, routes={
        '/': PageA(),
        '/b': PageB(),
        '/b/c': PageC()
    })

    router.install()


ft.app(target=main, view=ft.WEB_BROWSER, port=40444)
