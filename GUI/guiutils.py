from pathlib import Path
from GUI import gui


def relative_to_assets(path: str) -> Path:
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")
    return ASSETS_PATH / Path(path)


def delete_text_on_callback(event):  # note that you must include the event as an arg, even if you don't use it.
    event.widget.delete(0, "end")
    return None


