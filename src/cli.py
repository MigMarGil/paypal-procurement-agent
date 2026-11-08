import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm

from paypal_client import PayPalClient
from agent import ProcurementAgent

console = Console()

def main():
    parser = argparse.ArgumentParser(description="PayPal Autonomous Procurement Agent")
    parser.add_argument("command", choices=["buy", "audit"], help="Command to execute")
    parser.add_argument("--prompt", type=str, default="Cloud Server Infrastructure Setup", help="Purchase intent prompt")
    parser.add_argument("--amount", type=str, default=None, help="Override purchase amount")
    
    args = parser.parse_args()

    console.print(Panel.fit("[bold cyan]PayPal Autonomous Procurement Agent[/bold cyan]\n[dim]Agentic Commerce & Sandbox Execution Engine[/dim]", border_style="cyan"))

    agent = ProcurementAgent()
    paypal = PayPalClient()

    console.print(f"[yellow]Evaluating procurement intent:[/yellow] {args.prompt}")
    evaluation = agent.evaluate_intent(args.prompt)

    if args.amount:
        evaluation["amount"] = args.amount

    # Display Evaluation Report
    table = Table(title="AI Compliance & Guardrail Evaluation")
    table.add_column("Parameter", style="magenta")
    table.add_column("Value", style="green")

    table.add_row("Target Item", str(evaluation.get("item")))
    table.add_row("Calculated Cost", f"{evaluation.get('amount')} {evaluation.get('currency', 'USD')}")
    table.add_row("Risk Assessment", str(evaluation.get("risk_level")))
    table.add_row("Policy Approved", str(evaluation.get("approved")))
    table.add_row("AI Reasoning", str(evaluation.get("reasoning")))

    console.print(table)

    if not evaluation.get("approved", True):
        console.print("[bold red]Transaction blocked by local compliance guardrails.[/bold red]")
        sys.exit(1)

    if args.command == "audit":
        console.print("[bold green]Audit completed successfully. No live orders dispatched.[/bold green]")
        return

    # Execute PayPal Order Workflow
    if not Confirm.ask("[bold yellow]Do you want to proceed and execute this autonomous purchase in PayPal Sandbox?[/bold yellow]"):
        console.print("[red]Aborted by user.[/red]")
        sys.exit(0)

    try:
        console.print("[cyan]Initializing PayPal Sandbox API connection & dispatching agent...[/cyan]")
        
        # 1. Create Order (with direct automated payment source)
        order = paypal.create_order(
            amount=str(evaluation.get("amount")),
            currency=evaluation.get("currency", "USD"),
            description=str(evaluation.get("item"))
        )
        
        order_id = order.get("id")
        status = order.get("status")
        
        console.print(f"[green]✓ Order Processed Successfully![/green] ID: [bold]{order_id}[/bold] | Status: [bold]{status}[/bold]")

        capture_id = order_id # Direct capture in payment source maps cleanly
        if status != "COMPLETED":
            console.print("[cyan]Executing automated capture on Sandbox...[/cyan]")
            capture_result = paypal.capture_order(order_id)
            status = capture_result.get("status", "COMPLETED")

        success_panel = Panel(
            f"[bold green]Autonomous Commerce Transaction Completed![/bold green]\n\n"
            f"• [cyan]Order ID:[/cyan] {order_id}\n"
            f"• [cyan]Item Procured:[/cyan] {evaluation.get('item')}\n"
            f"• [cyan]Total Settled:[/cyan] {evaluation.get('amount')} {evaluation.get('currency', 'USD')}\n"
            f"• [cyan]Final Status:[/cyan] {status}\n"
            f"• [cyan]Environment:[/cyan] PayPal Sandbox",
            title="[bold]Agentic Settlement Receipt[/bold]",
            border_style="green"
        )
        console.print(success_panel)

    except Exception as e:
        console.print(f"[bold red]PayPal API Execution Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
