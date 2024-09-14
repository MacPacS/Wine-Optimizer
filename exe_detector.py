import os
import subprocess
import re

# Function to detect GPU and install drivers
def detect_gpu_and_install_drivers():
    try:
        # Get GPU information
        gpu_info = subprocess.check_output("lspci | grep -i vga", shell=True).decode('utf-8').lower()
        if "amd" in gpu_info:
            print("AMD GPU detected. Installing AMD drivers...")
            subprocess.run(['sudo', 'apt', 'install', '-y', 'xserver-xorg-video-amdgpu'], check=True)
        elif "nvidia" in gpu_info:
            print("Nvidia GPU detected. Installing Nvidia drivers...")
            subprocess.run(['sudo', 'apt', 'install', '-y', 'nvidia-driver-460'], check=True)
        else:
            print("No AMD or Nvidia GPU detected.")
    except Exception as e:
        print(f"Failed to detect or install GPU drivers: {str(e)}")

# Function to run Wine with the selected .exe and capture the log
def run_exe(exe_file):
    if not exe_file.endswith('.exe'):
        print("Please provide a valid .exe file.")
        return

    try:
        # Running the .exe file using Wine and capturing the output log
        process = subprocess.Popen(
            ['wine', exe_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        # Check for errors in Wine's logs
        error_lines = []
        for line in stderr.split('\n'):
            if "err:" in line.lower() or "fixme:" in line.lower():
                error_lines.append(line)

        # Display results
        if error_lines:
            print("\nErrors Detected:\n" + "\n".join(error_lines))
        else:
            print("\nNo errors found in Wine logs.")
        
        # Save log to file
        with open("wine_log.txt", "w") as log_file:
            log_file.write(stderr)
        print("Wine log saved as wine_log.txt.")

    except Exception as e:
        print(f"Error: {str(e)}")

# Function to install common drivers using winetricks
def install_drivers():
    driver_options = [
        ("DirectX", "dxvk"),
        ("Visual C++ Redistributables", "vcrun2015"),
        ("dotnet", "dotnet40"),
        ("Core Fonts", "corefonts")
    ]

    for driver_name, winetricks_option in driver_options:
        result = subprocess.run(['winetricks', winetricks_option], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{driver_name} installed successfully.")
        else:
            print(f"Failed to install {driver_name}.")

# Main function to handle command-line arguments and operations
def main():
    import argparse

    # Argument parsing
    parser = argparse.ArgumentParser(description="EXE Detector & Wine Log Checker for Terminal")
    parser.add_argument('-e', '--exe', type=str, help="Path to the .exe file", required=False)
    parser.add_argument('-d', '--drivers', action='store_true', help="Install common Wine drivers using winetricks")
    parser.add_argument('-g', '--gpu', action='store_true', help="Detect and install GPU drivers")

    args = parser.parse_args()

    if args.exe:
        run_exe(args.exe)

    if args.drivers:
        install_drivers()

    if args.gpu:
        detect_gpu_and_install_drivers()

if __name__ == '__main__':
    main()
