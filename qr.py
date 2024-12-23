import argparse
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress
import io
import requests
import os
import time
import platform
import json

console = Console()

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def upload_to_uguu(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'files[]': (os.path.basename(file_path), f)}
            response = requests.post('https://uguu.se/upload.php?output=text', files=files)
            if response.status_code == 200:
                return response.text.strip()
            console.print(f"[red]Upload failed with status code: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Upload error: {str(e)}[/red]")
    return None

def show_banner():
    clear_screen()
    console.print(Panel.fit(
        "[bold yellow]QR Code Generator & Scanner[/bold yellow]\n"
        "[blue]A CLI tool for QR code operations[/blue]",
        border_style="yellow"
    ))

def show_menu():
    table = Table(show_header=False, box=None)
    table.add_row("[1] Generate QR Code")
    table.add_row("[2] Scan QR Code")
    table.add_row("[3] Batch Generate QR Codes")
    table.add_row("[4] Exit")
    console.print(table)

def generate_qr(data, filename="generated_qr.png"):
    with Progress() as progress:
        task = progress.add_task("[cyan]Generating QR code...", total=100)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=2,
            border=1
        )
        progress.update(task, advance=30)
        
        qr.add_data(data)
        qr.make(fit=True)
        progress.update(task, advance=20)
        
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        ascii_qr = f.read()
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        progress.update(task, advance=25)
        
        # Upload to uguu.se
        console.print("\n[cyan]Uploading to uguu.se...[/cyan]")
        url = upload_to_uguu(filename)
        progress.update(task, advance=25)
    
    console.print(Panel(ascii_qr, title="Generated QR Code", border_style="green"))
    console.print(f"[green]QR code saved as '{filename}'[/green]")
    if url:
        console.print(f"[green]Uploaded to: {url}[/green]")
        console.print("[yellow]Note: The file will be available for 24 hours[/yellow]")
    else:
        console.print("[red]Failed to upload to uguu.se[/red]")
    
    return filename, url

def scan_qr(image_path):
    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning QR code...", total=100)
        
        try:
            if image_path.startswith(('http://', 'https://')):
                response = requests.get(image_path)
                img = Image.open(io.BytesIO(response.content))
            else:
                img = Image.open(image_path)
            
            progress.update(task, advance=50)
            decoded_objects = decode(img)
            progress.update(task, advance=50)
            
            if not decoded_objects:
                console.print("[red]No QR code found in image[/red]")
                return
            
            results_table = Table(title="Scan Results")
            results_table.add_column("Type", style="cyan")
            results_table.add_column("Data", style="green")
            
            for obj in decoded_objects:
                results_table.add_row(
                    obj.type,
                    obj.data.decode()
                )
            
            console.print(results_table)
            
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

def batch_generate():
    num_codes = int(Prompt.ask("\nHow many QR codes to generate", default="1"))
    base_name = Prompt.ask("Enter base filename", default="qr_code")
    
    urls = []
    for i in range(num_codes):
        data = Prompt.ask(f"\nEnter data for QR code {i+1}")
        filename = f"{base_name}_{i+1}.png"
        _, url = generate_qr(data, filename)
        if url:
            urls.append((filename, url))
        time.sleep(1)
    
    if urls:
        console.print("\n[yellow]Generated QR Codes URLs:[/yellow]")
        for filename, url in urls:
            console.print(f"[green]{filename}: {url}[/green]")

def main():
    parser = argparse.ArgumentParser(description="Enhanced QR Code Generator and Scanner")
    parser.add_argument('--generate', type=str, help='Generate QR code with specified data')
    parser.add_argument('--scan', type=str, help='Scan QR code from image path or URL')
    parser.add_argument('--batch', action='store_true', help='Batch generate multiple QR codes')
    args = parser.parse_args()

    if not (args.generate or args.scan or args.batch):
        while True:
            show_banner()
            show_menu()
            
            choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4"])
            
            if choice == "1":
                clear_screen()
                data = Prompt.ask("\nEnter data to encode")
                generate_qr(data)
                input("\nPress Enter to continue...")
            elif choice == "2":
                clear_screen()
                image_path = Prompt.ask("\nEnter image path or URL")
                scan_qr(image_path)
                input("\nPress Enter to continue...")
            elif choice == "3":
                clear_screen()
                batch_generate()
                input("\nPress Enter to continue...")
            else:
                clear_screen()
                console.print("[yellow]Thanks for using QR Code Tool![/yellow]")
                break
    else:
        if args.generate:
            generate_qr(args.generate)
        if args.scan:
            scan_qr(args.scan)
        if args.batch:
            batch_generate()

if __name__ == "__main__":
    main()
