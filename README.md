# FletRt

---

FletRt is a really simple routing solution for the Flet framework, developed mainly for personal use.

Flet is a Python framework for building cross-platform desktop applications with web technologies. FletRt allows you to
create multiple views for your Flet app and navigate between them using routes.

Please note that this project is still incomplete and lacks many features available on Flet.

This project core is slightly based off CodingJQ's [ Routing in Flet with Python in 3 Min (Tutorial) ](https://www.youtube.com/watch?v=mrmcIofA5bM)

### Installation

---

You can install FletRt by using the following command:

```bash
pip install fletrt
```

### Sample usage

---

#### main.py:

```python
import flet as ft
from fletrt import Router

from demo.page_a import PageA
from demo.page_b import PageB


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