from __future__ import annotations

import asyncio
from typing import Callable

import flet as ft


class AppTheme:
    """Global styles and colors for the JAMB Immunity app."""

    GLOW_BLUE = "#4CC9F0"
    VICTORY_GOLD = "#FFD166"
    CALM_PURPLE = "#8A6BFF"
    STRESS_RED = "#FF4D6D"
    BACKGROUND_DARK = "#090B17"
    GLASS_BG = "#24FFFFFF"  # Semi-transparent white (glassmorphism)

    HEADLINE = ft.TextStyle(
        size=34,
        weight=ft.FontWeight.W_700,
        color=ft.Colors.WHITE,
        letter_spacing=0.5,
    )
    BODY = ft.TextStyle(
        size=16,
        weight=ft.FontWeight.W_400,
        color="#D7DEFF",
    )
    GLOW_TEXT = ft.TextStyle(
        size=20,
        weight=ft.FontWeight.W_600,
        color=GLOW_BLUE,
    )

    @staticmethod
    def apply_theme(page: ft.Page) -> None:
        """Apply global theme settings to a Flet page."""

        page.title = "JAMB Immunity • The Oracle AI"
        page.bgcolor = AppTheme.BACKGROUND_DARK
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 24
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=AppTheme.GLOW_BLUE,
                secondary=AppTheme.CALM_PURPLE,
                error=AppTheme.STRESS_RED,
                background=AppTheme.BACKGROUND_DARK,
            ),
            text_theme=ft.TextTheme(
                headline_large=AppTheme.HEADLINE,
                body_large=AppTheme.BODY,
            ),
            visual_density=ft.ThemeVisualDensity.COMFORTABLE,
        )


class GlowingCard(ft.Container):
    def __init__(
        self,
        content: ft.Control,
        width: float = 360,
        height: float = 220,
        glow_color: str = AppTheme.GLOW_BLUE,
    ) -> None:
        super().__init__()
        self._glow_color = glow_color
        self.content = content
        self.width = width
        self.height = height
        self.padding = 20
        self.border_radius = 22
        self.bgcolor = AppTheme.GLASS_BG
        self.border = ft.border.all(1.3, ft.Colors.with_opacity(0.25, glow_color))
        self.blur = 10
        self.shadow = [
            ft.BoxShadow(
                spread_radius=1,
                blur_radius=14,
                color=ft.Colors.with_opacity(0.28, glow_color),
            )
        ]
        self.animate = ft.Animation(260, ft.AnimationCurve.EASE_OUT)
        self.on_hover = self._on_hover

    def _on_hover(self, e: ft.HoverEvent) -> None:
        hovered = e.data == "true"
        self.shadow = [
            ft.BoxShadow(
                spread_radius=2 if hovered else 1,
                blur_radius=34 if hovered else 14,
                color=ft.Colors.with_opacity(0.6 if hovered else 0.28, self._glow_color),
            )
        ]
        self.border = ft.border.all(
            1.8 if hovered else 1.3,
            ft.Colors.with_opacity(0.95 if hovered else 0.25, self._glow_color),
        )
        self.update()


class GlowingButton(ft.Container):
    def __init__(
        self,
        text: str,
        on_click: Callable[[ft.ControlEvent], None],
        color: str = AppTheme.CALM_PURPLE,
        icon: str | None = None,
    ) -> None:
        super().__init__()
        self._base_color = color
        self.border_radius = 18
        self.ink = True
        self.padding = ft.padding.symmetric(horizontal=18, vertical=14)
        self.bgcolor = ft.Colors.with_opacity(0.22, color)
        self.animate = ft.Animation(220, ft.AnimationCurve.EASE_OUT)
        self.on_hover = self._on_hover
        self.shadow = [
            ft.BoxShadow(
                blur_radius=16,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.35, color),
            )
        ]

        label = ft.Row(
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Icon(icon, color=ft.Colors.WHITE, size=18) if icon else ft.Container(width=0, height=0),
                ft.Text(text, style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)),
            ],
        )
        self.content = ft.GestureDetector(content=label, on_tap=on_click)

    def _on_hover(self, e: ft.HoverEvent) -> None:
        hovered = e.data == "true"
        self.bgcolor = ft.Colors.with_opacity(0.35 if hovered else 0.22, self._base_color)
        self.shadow = [
            ft.BoxShadow(
                blur_radius=30 if hovered else 16,
                spread_radius=2 if hovered else 1,
                color=ft.Colors.with_opacity(0.75 if hovered else 0.35, self._base_color),
            )
        ]
        self.update()


class GlowingText(ft.Stack):
    def __init__(
        self,
        text: str,
        size: float = 28,
        weight: ft.FontWeight = ft.FontWeight.W_700,
        glow: str = AppTheme.GLOW_BLUE,
    ) -> None:
        self.glow_layer = ft.Text(
            text,
            size=size,
            weight=weight,
            color=ft.Colors.with_opacity(0.55, glow),
            animate_opacity=ft.Animation(900, ft.AnimationCurve.EASE_IN_OUT),
        )
        main_layer = ft.Text(text, size=size, weight=weight, color=ft.Colors.WHITE)

        super().__init__(controls=[self.glow_layer, main_layer])

    def pulse(self, intense: bool) -> None:
        self.glow_layer.opacity = 1.0 if intense else 0.45
        self.update()


def AnimatedBackground() -> tuple[ft.Stack, ft.Ref[ft.Container], ft.Ref[ft.Container]]:
    """Create layered gradient controls to animate the page background."""

    layer_1 = ft.Ref[ft.Container]()
    layer_2 = ft.Ref[ft.Container]()

    background = ft.Stack(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#05060D", "#0B1235", "#070A1A"],
                ),
            ),
            ft.Container(
                ref=layer_1,
                width=900,
                height=900,
                left=-250,
                top=-300,
                border_radius=450,
                bgcolor=ft.Colors.with_opacity(0.14, AppTheme.GLOW_BLUE),
                blur=120,
                animate_position=ft.Animation(4500, ft.AnimationCurve.EASE_IN_OUT),
                animate_opacity=ft.Animation(1800, ft.AnimationCurve.EASE_IN_OUT),
            ),
            ft.Container(
                ref=layer_2,
                width=850,
                height=850,
                right=-260,
                bottom=-350,
                border_radius=425,
                bgcolor=ft.Colors.with_opacity(0.12, AppTheme.CALM_PURPLE),
                blur=120,
                animate_position=ft.Animation(4200, ft.AnimationCurve.EASE_IN_OUT),
                animate_opacity=ft.Animation(1600, ft.AnimationCurve.EASE_IN_OUT),
            ),
        ],
    )
    return background, layer_1, layer_2


def main(page: ft.Page) -> None:
    AppTheme.apply_theme(page)

    background, layer_1, layer_2 = AnimatedBackground()

    title = GlowingText("Welcome to The Oracle AI", size=36, glow=AppTheme.VICTORY_GOLD)

    card = GlowingCard(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Text("JAMB Immunity", style=AppTheme.HEADLINE),
                ft.Text(
                    "Futuristic CBT practice with adaptive hints, focus analytics, and confidence tracking.",
                    style=AppTheme.BODY,
                ),
            ],
        ),
        width=620,
        height=220,
        glow_color=AppTheme.GLOW_BLUE,
    )

    def _clicked(_: ft.ControlEvent) -> None:
        page.snack_bar = ft.SnackBar(ft.Text("The Oracle AI is warming up..."), open=True)
        page.update()

    cta = GlowingButton("Start Weekly Access • ₦500", on_click=_clicked, color=AppTheme.VICTORY_GOLD, icon=ft.Icons.BOLT)

    content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=24,
        controls=[title, card, cta],
    )

    page.add(
        ft.Stack(
            expand=True,
            controls=[
                background,
                ft.Container(content=content, alignment=ft.alignment.center, expand=True),
            ],
        )
    )

    async def animate() -> None:
        intense = False
        while True:
            intense = not intense
            if layer_1.current and layer_2.current:
                layer_1.current.top = -220 if intense else -320
                layer_1.current.left = -210 if intense else -260
                layer_1.current.opacity = 1.0 if intense else 0.75

                layer_2.current.bottom = -280 if intense else -360
                layer_2.current.right = -200 if intense else -260
                layer_2.current.opacity = 1.0 if intense else 0.7

                layer_1.current.update()
                layer_2.current.update()

            title.pulse(intense)
            await asyncio.sleep(2.0)

    page.run_task(animate)


if __name__ == "__main__":
    ft.app(target=main)
