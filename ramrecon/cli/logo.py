from rich.console import Console
from rich.panel import Panel
from rich.align import Align

RED = "#ef4444"

console = Console()


def logo(version: str, modules: int, author: str) -> None:
    art = r"""
██████╗  █████╗ ███╗   ███╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝███████║██╔████╔██║██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══██║██║╚██╔╝██║██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
""".strip("\n")

    colored_art = "\n".join(
        f"[bold {RED}]{line}[/bold {RED}]"
        for line in art.splitlines()
    )

    subtitle = (
        f"[bold white]Cyber Reconnaissance & Intelligence Framework[/bold white]\n\n"
        f"[bold green]Version:[/bold green] {version}    "
        f"[bold yellow]Modules:[/bold yellow] {modules}    "
        f"[bold magenta]Author:[/bold magenta] {author}"
    )

    panel_content = f"{colored_art}\n\n{subtitle}"

    console.print(
        Align.center(
            Panel(
                panel_content,
                border_style=RED,
                padding=(1, 3),
                title="[bold white]RAMRecon[/bold white]",
                subtitle="[bold cyan]Reconnaissance • Analysis • Intelligence[/bold cyan]",
            )
        )
    )

    console.print(
        f"[bold {RED}]Type 'help' to see available commands.[/bold {RED}]"
    )