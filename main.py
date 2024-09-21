import requests
from termcolor import colored
import argparse
import threading
import logging
import os
import signal
import sys


# Define proxies if using a proxy (like Burp Suite)
#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
logging.basicConfig(level=logging.INFO, format=" %(levelname)s - %(message)s")

intense_red = "\033[31;1m"
intense_green = "\033[32;1m"
intense_blue = "\033[34;1m"
intense_yellow = "\033[33;1m"
intense_cyan = "\033[36;1m"
intense_magenta = "\033[35;1m"
reset = "\033[0m"

def exit_handler(sig, frame):
    print(f"{intense_yellow}Exiting ... {reset}")
    exit()

signal.signal(signal.SIGINT, exit_handler)

# To store vulnerable URLs
vulnerable_urls = []

# Function to center the banner in the terminal
def banner():
    terminal_width = os.get_terminal_size().columns

    # Banner lines
    line1 = f"{intense_cyan}----------------------------------------------------------------------{reset}"
    line2 = f"{intense_magenta}|   Welcome to the LFI Vulnerability Scanner | Author: Jamaal Ahmed  |{reset}"
    line3 = f"{intense_cyan}----------------------------------------------------------------------{reset}"

    # Calculate center padding based on terminal width
    print(line1.center(terminal_width))
    print(line2.center(terminal_width))
    print(line3.center(terminal_width))

# Function to send a request and get the response text
def get_response_text(full_url):
    try:
        response = requests.get(full_url)
        return response.text
    except requests.exceptions.RequestException as e:
        print(colored(f"[-] Error: {e}", "red"))
        return None

# Main function to compare the baseline response and payload response
def main(url, file_payloads, baseline_response):
    full_url = url + file_payloads

    # Get the response after adding the payload
    payload_response = get_response_text(full_url)

    if payload_response != baseline_response:
        logging.info(f"{intense_green}[*] Vulnerable: {reset} {intense_yellow}{full_url}{reset}")
        vulnerable_urls.append(full_url)  # Store the vulnerable URL
    else:
        logging.info(f"{intense_red}[-] Not Vulnerable: {reset} {intense_yellow}{full_url}{reset}")

# Argument parsing to get the target URL and payloads file
if __name__ == "__main__":
    banner()  # Show banner at the start

    parser = argparse.ArgumentParser(description="Welcome to the Simple LFI Scanner Script.")
    parser.add_argument("-u", "--url", required=True, help="Specify the target URL (e.g., http://example.com/vuln?file=)")
    parser.add_argument("-p", "--payloads", required=True, help="Specify the file containing the list of payloads")

    args = parser.parse_args()

    url = args.url
    file_payloads = args.payloads

    # Get the baseline response without any payload
    baseline_response = get_response_text(url)

    if not baseline_response:
        print(colored("[-] Failed to get the baseline response.", "red"))
        exit()

    # Reading the payloads from the specified file
    with open(file_payloads, "r") as file:
        jamaal = file.read().splitlines()

        # Create a list to hold threads
        threads = []

        # Create and start a thread for each payload
        for last in jamaal:
            thread = threading.Thread(target=main, args=(url, last, baseline_response))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        logging.info(f"{intense_cyan}[+] Process finished.{reset}")

        # Display number of vulnerable URLs found
        print(f"{intense_cyan}------------------------------------------{reset}")
        if vulnerable_urls:
            print(f"{intense_green}[*] Vulnerable URLs found: {len(vulnerable_urls)}{reset}")
        else:
            print(f"{intense_red}[-] No vulnerabilities found.{reset}")
        print(f"{intense_cyan}------------------------------------------{reset}")
