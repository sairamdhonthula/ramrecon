from rich.console import Console
from rich.panel import Panel
from rich.align import Align

TEAL = "#2EC4B6"

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
        f"[bold {TEAL}]{line}[/bold {TEAL}]"
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
                border_style=TEAL,
                padding=(1, 3),
                title="[bold white]RAMRecon[/bold white]",
                subtitle="[bold cyan]Reconnaissance • Analysis • Intelligence[/bold cyan]",
            )
        )
    )

    console.print(
        f"[bold {TEAL}]Type 'help' to see available commands.[/bold {TEAL}]"
    )