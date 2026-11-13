from keyhac import SnapWindow  # ty: ignore[unresolved-import]


def bind(keymap, kt) -> None:

    kt_snap = keymap.define_keytable(name="Snap active window")
    kt_snap["U0-L"] = "LWin-Shift-Right"
    kt_snap["U0-H"] = "LWin-Shift-Left"

    def minimize() -> None:
        wnd = keymap.get_active_window()
        if wnd:
            wnd.minimize()

    kt_snap["N"] = minimize

    def maximize() -> None:
        wnd = keymap.get_active_window()
        if wnd:
            wnd.maximize()

    kt_snap["X"] = maximize

    class SnapToScreen:
        def __init__(self, screen_index: int) -> None:
            self._screen_index = screen_index

        def __call__(self) -> None:
            active_wnd = keymap.get_active_window()
            if active_wnd is None:
                return

            screen_frames = keymap.screen_work_frames()
            try:
                target_frame = screen_frames[self._screen_index]
            except IndexError:
                return

            if active_wnd.is_maximized():
                active_wnd.restore()

            current = active_wnd.get_frame()
            if current is None:
                return

            sx, sy, sw, sh = target_frame
            _, _, ww, wh = current
            x = sx + (sw - ww) / 2
            y = sy + (sh - wh) / 2
            if not active_wnd.set_frame(x, y):
                return

            active_wnd.maximize()

    for i in (0, 1, 2):
        kt_snap[str(i)] = SnapToScreen(i)

    for mod, ratio in {
        "": 1 / 2,
        "S-": 2 / 3,
        "C-": 1 / 3,
    }.items():
        for key, position in {
            "H": "left",
            "L": "right",
            "J": "bottom",
            "K": "top",
        }.items():
            kt_snap[mod + key] = SnapWindow(position=position, ratio=ratio)

    class WindowHalfResizer:
        def __init__(self, direction: str) -> None:
            if direction not in ("left", "right", "up", "down"):
                raise ValueError(f"invalid direction: {direction}")

            self.direction = direction
            self.min_pixel = 200

        def __call__(self) -> None:
            active_wnd = keymap.get_active_window()
            if active_wnd is None:
                return

            current_frame = active_wnd.get_frame()
            x, y, w, h = current_frame
            half_w = w // 2
            half_h = h // 2

            if (self.direction in ("left", "right") and half_w < self.min_pixel) or (
                self.direction in ("up", "down") and half_h < self.min_pixel
            ):
                return

            new_frame = current_frame
            if self.direction == "left":
                new_frame = (x, y, half_w, h)
            elif self.direction == "right":
                new_frame = (x + half_w, y, half_w, h)
            elif self.direction == "up":
                new_frame = (x, y, w, half_h)
            elif self.direction == "down":
                new_frame = (x, y + half_h, w, half_h)

            active_wnd.set_frame(*new_frame)

    for key, direction in {
        "H": "left",
        "L": "right",
        "J": "down",
        "K": "up",
    }.items():
        kt_snap[f"U1-{key}"] = WindowHalfResizer(direction)

    kt["U1-M"] = kt_snap

    kt["U1-H"] = SnapWindow(position="left")
    kt["U1-L"] = SnapWindow(position="right")
