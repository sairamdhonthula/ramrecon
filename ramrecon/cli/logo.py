import time
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

def startup_sequence(no_animation: bool = False) -> None:
    if no_animation:
        os.system("cls" if os.name == "nt" else "clear")
        return

    os.system("cls" if os.name == "nt" else "clear")
    
    # Render the Initializing box using Rich Panel for maximum beauty
    boot_text = (
        f"[bold white]Initializing RAMRecon v2.0[/bold white]\n"
        f"[dim white]Cyber Recon & Intelligence[/dim white]"
    )
    console.print(
        Align.center(
            Panel(
                boot_text,
                border_style=TEAL,
                padding=(1, 4),
                expand=False,
            )
        )
    )
    print()
    time.sleep(0.4)
    
    stages = ["SCAN", "DNS", "TLS", "INTEL"]
    line_len = 25
    indent = " " * 8
    
    # Animate each stage
    for stage in stages:
        stage_str = f"[{stage}]".ljust(7)
        for step in range(line_len + 1):
            before = "─" * step
            after = "─" * (line_len - step)
            if step == line_len:
                console.print(f"{indent}{stage_str}{before}► [bold {TEAL}][RAMRecon][/bold {TEAL}]", end="\r")
            else:
                console.print(f"{indent}{stage_str}{before}●{after}► RAMRecon", end="\r")
            time.sleep(0.01)
        print()
        time.sleep(0.05)
        
    time.sleep(0.2)
    os.system("cls" if os.name == "nt" else "clear")


RED = "#ef4444"
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
                border_style=RED,
                padding=(1, 3),
                title="[bold white]RAMRecon[/bold white]",
                subtitle="[bold cyan]Reconnaissance • Analysis • Intelligence[/bold cyan]",
                expand=False,
            )
        )
    )

    console.print(
        f"[bold {RED}]Type 'help' to see available commands.[/bold {RED}]"
    )