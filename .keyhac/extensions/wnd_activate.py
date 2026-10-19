import os
import shutil
from pathlib import Path
from typing import NamedTuple

from keyhac import (  # ty: ignore[unresolved-import]
    ActivateApplication,
    Candidate,
    CandidateSource,
    ChooserPage,
    ShowCandidates,
)
from libs.system_browser import get_browser_path


class LaunchEntry(NamedTuple):
    app: str
    launch: str | None

    def as_params(self) -> dict:
        params = {"app": self.app}
        if self.launch is not None:
            params["launch"] = os.path.expandvars(self.launch)
        return params


SINGLE_KEY_MAPPING: dict[str, LaunchEntry] = {
    "U1-F": LaunchEntry(
        "cfiler",
        r"${USERPROFILE}\Personal\portable_apps\cfiler\cfiler.exe",
    ),
    "U1-P": LaunchEntry("SumatraPDF", None),
    "LC-U1-M": LaunchEntry(
        "Mery",
        r"${LOCALAPPDATA}\Programs\Mery\Mery.exe",
    ),
    "LC-U1-N": LaunchEntry(
        "notepad",
        r"C:\Windows\System32\notepad.exe",
    ),
    "LC-AtMark": LaunchEntry(
        "wezterm-gui",
        r"${USERPROFILE}\scoop\apps\wezterm\current\wezterm-gui.exe",
    ),
}

MULTI_KEY_MAPPING: dict[str, LaunchEntry] = {
    "C": LaunchEntry(
        "chrome",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ),
    "Comma": LaunchEntry("smoothcsv-app", None),
    "S": LaunchEntry(
        "slack",
        r"${LOCALAPPDATA}\slack\slack.exe",
    ),
    "F": LaunchEntry(
        "firefox",
        r"C:\Program Files\Mozilla Firefox\firefox.exe",
    ),
    "B": LaunchEntry(
        "thunderbird",
        r"C:\Program Files (x86)\Mozilla Thunderbird\thunderbird.exe",
    ),
    "P": LaunchEntry("SumatraPDF", None),
    "E": LaunchEntry("EXCEL", None),
    "W": LaunchEntry("WINWORD", None),
}

if (code_path := shutil.which("code")) is not None:
    MULTI_KEY_MAPPING["V"] = LaunchEntry("Code.exe", code_path)

if (browser_path := get_browser_path()) is not None:
    MULTI_KEY_MAPPING["Space"] = LaunchEntry(Path(browser_path).name, browser_path)


def bind(keymap, kt) -> None:

    for key, entry in SINGLE_KEY_MAPPING.items():
        kt[key] = ActivateApplication(**entry.as_params())

    kt_second_key = keymap.define_keytable()
    for key, entry in MULTI_KEY_MAPPING.items():
        kt_second_key[key] = ActivateApplication(**entry.as_params())

    kt["U1-C"] = kt_second_key

    class OpenWindows(CandidateSource):
        name = "Window"

        def candidates(self):
            wnd = keymap.get_active_window()

            def _is_candidate(w) -> bool:
                if not w.title:
                    return False
                if wnd is None:
                    return True
                return wnd.title != w.title

            return [
                Candidate(display=f"{w.app_name} - {w.title}", payload=w)
                for w in keymap.list_windows()
                if _is_candidate(w)
            ]

        def on_chosen(self, candidate, _):
            candidate.payload.activate()

    kt["U1-E"] = ShowCandidates([ChooserPage("Windows", [OpenWindows()])])
