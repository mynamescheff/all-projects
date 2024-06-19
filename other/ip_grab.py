#grab IP and mac address of all devices on the network and append to a file with date and time stamp
import os
import time
import subprocess
import re

def get_ip_mac():
    # Get the current date and time
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Run the arp command to get the IP and MAC addresses
    arp_output = subprocess.check_output(["arp", "-a"]).decode("utf-8")
    
    # Regular expression to match IP and MAC addresses
    pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9A-Fa-f:]+)")
    
    # Find all matches in the arp output
    matches = pattern.findall(arp_output)
    
    # Append the IP and MAC addresses to a file with the current date and time
    #save it to the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "ip_mac_addresses.txt")

    #add devices names to the file as well
    with open(file_path, "a") as file:
        file.write(f"Date and Time: {now}\n")
        for ip, mac in matches:
            file.write(f"IP Address: {ip}, MAC Address: {mac}\n")
        file.write("\n")

    print("IP and MAC addresses saved to ip_mac_addresses.txt")


# Run the function to get IP and MAC addresses
get_ip_mac()
