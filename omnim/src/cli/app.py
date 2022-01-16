import typer

app = typer.Typer()


@app.command()
def main(
    metrics: str = typer.Option("", help=""),
    input_file: str = ""
):
    typer.echo(f"Hello")

if __name__ == "__main__":
    app()