# FletRT

---

A really simple routing solution for the [Flet](https://flet.dev) framework, developed mainly for personal use.

Please note that this project is still incomplete and lacks many features available on flet. 

### Sample usage:

---

#### main.py:

```python
import flet as ft
from fletrt import Router


def main(page: ft.Page):
    Router(page, routes={
        '/page-a': PageA(),
        '/page-b': PageB()
    }, starting_route='/page-a')


ft.app(target=main)
```

#### page_a.py:
```python
import flet as ft
from fletrt import RouteView

class PageA(RouteView):
    def body(self) -> ft.Container:

        return ft.Container(
            ft.Column(
                controls=[
                    ft.Text("Hello World, from Page A!"),
                    ft.ElevatedButton("Go to Page B", on_click=lambda _: self._page.go('/page-b'))
                ]
            )
        )
```

#### page_b.py:
```python
import flet as ft
from fletrt import RouteView

class PageB(RouteView):
    def body(self) -> ft.Container:

        return ft.Container(
            ft.Column(
                controls=[
                    ft.Text("Hello World, from Page B!"),
                ]
            )
        )
```