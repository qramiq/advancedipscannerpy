def save_results_to_file(file_name, results):
    with open(file_name, 'w') as f:
        f.write("Advanced IP Scanner Results\n")
        f.write("=" * 50 + "\n\n")
        
        for device in results:
            f.write(f"Status: {device['status']}\n")
            f.write(f"Name: {device['name']}\n")
            f.write(f"IP: {device['ip']}\n")
            f.write(f"Manufacturer: {device['manufacturer']}\n")
            f.write(f"MAC Address: {device['mac']}\n")
            f.write("-" * 50 + "\n")

