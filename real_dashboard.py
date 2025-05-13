from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Grid
from textual.reactive import reactive
from rich.text import Text
from datetime import datetime
import subprocess
import threading
import os
import sys
import queue

class NodePanel(Static):
    """A panel displaying output from a running script, with optional startup delay."""
    log = reactive("")

    def __init__(self, title: str, script_cmd: list, start_delay: float = 0, id: str = None):
        super().__init__(id=id)
        self.title = title
        self.script_cmd = script_cmd
        self.start_delay = start_delay
        self.process = None
        self.output_queue = queue.Queue()
        self.running = False

    def on_mount(self):
        """Schedule the script start after a delay."""
        if self.start_delay > 0:
            self.set_timer(self.start_delay, self._start_with_delay)
        else:
            self._start_with_delay()

    def _start_with_delay(self):
        self.running = True
        self.update(Text(f"{self.title}\nStarting...", style="bold underline cyan"))
        threading.Thread(target=self._run_script, daemon=True).start()
        self.set_interval(0.1, self._update_log)

    def _run_script(self):
        """Run the script and capture output."""
        try:
            self.process = subprocess.Popen(
                self.script_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=os.path.dirname(os.path.abspath(__file__)),
            )
            for line in self.process.stdout:
                if not self.running:
                    break
                self.output_queue.put(line.strip())
            for line in self.process.stderr:
                if not self.running:
                    break
                self.output_queue.put(f"[ERROR] {line.strip()}")
            self.process.wait()
        except Exception as e:
            self.output_queue.put(f"[ERROR] Failed to run {self.title}: {e}")

    def _update_log(self):
        """Update the panel with new log messages."""
        updated = False
        while not self.output_queue.empty():
            message = self.output_queue.get()
            now = datetime.now().strftime("%H:%M:%S")
            self.log += f"[{now}] {message}\n"
            if len(self.log.splitlines()) > 20:
                self.log = "\n".join(self.log.splitlines()[-20:])
            updated = True

        if updated:
            last_msg = self.log.splitlines()[-1].lower()
            if "alert" in last_msg or "deleted" in last_msg:
                color = "red"
            elif "modified" in last_msg:
                color = "yellow"
            elif "connected" in last_msg or "waiting" in last_msg:
                color = "cyan"
            elif "error" in last_msg:
                color = "red"
            else:
                color = "white"

            txt = Text(f"{self.title}\n", style=f"bold underline {color}")
            txt.append(self.log)
            self.update(txt)

    def on_unmount(self):
        """Stop the script when the panel is unmounted."""
        self.running = False
        if self.process:
            self.process.terminate()
            self.process.wait()

class ManetDashboard(App):
    """Textual app to display MANET simulation outputs with custom layout."""
    CSS = """
    Grid#top {
        grid-size: 1;
        grid-gutter: 1;
        padding: 1;
        background: $panel;
    }
    Grid#bottom {
        grid-size: 4;
        grid-gutter: 1;
        padding: 1;
        background: $panel;
    }

    Static {
        border: round green;
        padding: 1;
        height: 20;
        overflow: auto;
        background: black;
        color: white;
    }

    Static#key_manager { border: round cyan; }
    Static#node_x1, Static#node_x2, Static#node_x3 { border: round yellow; }
    Static#admin_node { border: round blue; }
    """

    def compose(self) -> ComposeResult:
        """Compose the dashboard with a top and bottom grid."""
        project_dir = os.path.dirname(os.path.abspath(__file__))
        python_exe = sys.executable

        # Top row: Key Manager alone
        yield Grid(
            NodePanel(
                "Key Manager",
                [python_exe, os.path.join(project_dir, "key_manager2.py")],
                start_delay=0,
                id="key_manager"
            ),
            id="top"
        )

        # Bottom row: Nodes and Admin in one line
        yield Grid(
            NodePanel(
                "Node_X1",
                [python_exe, os.path.join(project_dir, "nodes_test.py"), "Node_X1", "127.0.0.2", "5559", "NODE1"],
                start_delay=3,
                id="node_x1"
            ),
            NodePanel(
                "Node_X2",
                [python_exe, os.path.join(project_dir, "nodes_test.py"), "Node_X2", "127.0.0.2", "5560", "NODE2"],
                start_delay=6,
                id="node_x2"
            ),
            NodePanel(
                "Node_X3",
                [python_exe, os.path.join(project_dir, "nodes_test.py"), "Node_X3", "127.0.0.2", "5561", "NODE3"],
                start_delay=9,
                id="node_x3"
            ),
            NodePanel(
                "Admin Node",
                [python_exe, os.path.join(project_dir, "nodes_test.py"), "ADMIN", "127.0.0.2", "5599", "ADMIN"],
                start_delay=12,
                id="admin_node"
            ),
            id="bottom"
        )

    def on_mount(self):
        """Set the app title."""
        self.title = "MANET Network Intrusion Detection Dashboard"

if __name__ == "__main__":
    ManetDashboard().run()

