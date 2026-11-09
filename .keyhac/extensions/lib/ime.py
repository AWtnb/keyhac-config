from enum import StrEnum


def setup(_keymap) -> None:
    global keymap  # ty: ignore[unresolved-global]
    keymap = _keymap


def get_status() -> bool | None:
    return keymap.get_ime_status()


def set_status(status: bool) -> bool:
    return keymap.set_ime_status(status)


class SKKKey(StrEnum):
    toggle_vk = "(243)"
    kata = "Q"
    kana = "C-J"
    halfkata = "C-O"
    latin = "S-L"
    cancel = "Esc"
    reconv = "LWin-Slash"
    abbrev = "Slash"
    convpoint = "S-0"
    jlatin = "S-Q"
    affix = "S-Period"


def enable_ime() -> bool:
    status = get_status()
    if status is None:
        return False
    if status:
        return True
    return set_status(True)


def disable_ime() -> bool:
    status = get_status()
    if status is None:
        return False
    if status:
        return set_status(False)
    return True


def _send_ime_sequence(*seq: str) -> bool:
    """
    IMEを有効にしてキー入力でSKKを初期化する
    """
    if enable_ime():
        with keymap.get_input_context() as ctx:
            for key in (SKKKey.kana, *seq):
                ctx.send_key(key)
        return True
    return False


def to_skk_kana() -> bool:
    return _send_ime_sequence()


def to_skk_latin() -> bool:
    return _send_ime_sequence(SKKKey.latin)


def to_skk_abbrev() -> bool:
    return _send_ime_sequence(SKKKey.abbrev)


def to_skk_kata() -> bool:
    return _send_ime_sequence(SKKKey.kata)


def to_skk_half_kata() -> bool:
    return _send_ime_sequence(SKKKey.halfkata)


def to_skk_full_latin() -> bool:
    return _send_ime_sequence(SKKKey.jlatin)


def start_skk_conv() -> bool:
    return _send_ime_sequence(SKKKey.convpoint)


def start_skk_conv_suffix() -> bool:
    return _send_ime_sequence(SKKKey.convpoint, SKKKey.affix)


def reconvert_with_skk() -> bool:
    return _send_ime_sequence(SKKKey.reconv, SKKKey.cancel)
