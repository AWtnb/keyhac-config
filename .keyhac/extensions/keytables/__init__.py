from . import browser, excel, mery, slack, smoothcsv, sumatra_pdf, vscode


def setup(keymap) -> None:
    for kt in [
        browser,
        mery,
        slack,
        smoothcsv,
        sumatra_pdf,
        vscode,
        excel,
    ]:
        kt.bind(keymap)
