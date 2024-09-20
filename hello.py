import socket
import threading
from colorama import Fore, Style, init
import datetime


init(autoreset=True)

def scan_port(ip, port, results, lock):
    """
    Function to scan a single port on the specified IP address.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  
    try:
        result = sock.connect_ex((ip, port))
        with lock:
            if result == 0:
                results.append(port)
                print(f"{Fore.GREEN}{ip}:{port}")  
            else:
                print(f"{Fore.RED}Port {port} is closed", end='\r')
    except Exception as e:
        print(f"{Fore.RED}Error scanning port {port}: {e}")
    finally:
        sock.close()

def scan_ports(ip, start_port, end_port, output_file):
    """
    Function to scan a range of ports on the specified IP address.
    """
    results = []
    threads = []
    lock = threading.Lock()

    print(f"\nScanning ports {start_port} to {end_port}...")
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, results, lock))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    if results:
        print(f"\n{Fore.GREEN}Open ports: {', '.join([f'{ip}:{port}' for port in results])}")
        with open(output_file, 'w') as f:
            for port in results:
                f.write(f"{ip}:{port}\n")  
        print(f"\n{Fore.CYAN}Results saved to {output_file}")
    else:
        print(f"\n{Fore.RED}No open ports found")

if __name__ == "__main__":
    ip_input = input("Enter the IP address to scan: ")


    if ':' in ip_input:
        ip, port = ip_input.split(':')
        start_port = int(port)
        end_port = int(port)
    else:
        ip = ip_input
        start_port = 1
        end_port = 65535
    

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"open_ports_{current_time}.txt"
    
    scan_ports(ip, start_port, end_port, output_file)
