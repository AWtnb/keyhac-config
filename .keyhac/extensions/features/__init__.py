from . import (
    clipboard,
    core,
    ime,
    mouse_cursor,
    sender,
    web_search,
    wnd_activate,
    wnd_snap,
)


def setup(keymap, kt) -> None:
    for module in [
        core,
        clipboard,
        ime,
        sender,
        mouse_cursor,
        web_search,
        wnd_activate,
        wnd_snap,
    ]:
        module.bind(keymap, kt)
