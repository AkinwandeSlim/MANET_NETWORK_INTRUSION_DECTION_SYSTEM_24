from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Grid
from textual.reactive import reactive
from textual.timer import Timer
from datetime import datetime
import random

SAMPLE_MESSAGES = [
    "[green]No Change Detected",
    "[red]ALERT: File Deleted",
    "[yellow]ALERT: File Modified",
    "[cyan]Connected to MANET",
    "[magenta]Routing message to ADMIN...",
]

class NodePanel(Static):
    """A panel simulating a node or admin output."""
    log = reactive("")

    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.timer: Timer | None = None

    def on_mount(self):
        self.timer = self.set_interval(2, self._simulate_log_update)

    def _simulate_log_update(self):
        message = random.choice(SAMPLE_MESSAGES)
        self.update_log(message)

    def update_log(self, message: str):
        now = datetime.now().strftime("%H:%M:%S")
        self.log += f"[bold]{now}[/bold] {message}\n"
        if len(self.log.splitlines()) > 10:
            self.log = "\n".join(self.log.splitlines()[-10:])
        self.update(f"[bold underline]{self.title}[/]\n{self.log}")

class ManetDashboard(App):
    CSS = """
    Grid {
        grid-size: 2;
        grid-gutter: 1;
        padding: 1;
    }

    Static {
        border: round green;
        padding: 1;
        height: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        with Grid():
            yield NodePanel("Node_X1")
            yield NodePanel("Node_X2")
            yield NodePanel("Key Manager")
            yield NodePanel("ADMIN")

if __name__ == "__main__":
    ManetDashboard().run()
