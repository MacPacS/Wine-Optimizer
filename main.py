import os
import subprocess

print("""
    __    _                  ____     __                __
   / /   (_)___  __  ___  __/  _/____/ /___ _____  ____/ /
  / /   / / __ \/ / / / |/_/ / // ___/ / __ `/ __ \/ __  / 
 / /___/ / / / / /_/ />  </ // /__  ) / /_/ / / / / /_/ /  
/_____/_/_/ /_/\__,_/_/|_/___/____/_/\__,_/_/ /_/\__,_/   
""")

print("Created by MacPacS")


def list_sh_files():
    # Get all .sh files in the current directory
    sh_files = [f for f in os.listdir('.') if f.endswith('.sh')]
    if not sh_files:
        print("No .sh files found in the current directory.")
        return None
    return sh_files

def display_files(files):
    # Display the list of .sh files
    print("Available .sh files:")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

def choose_file(files):
    # Ask the user to choose a file
    try:
        choice = int(input("Enter the number of the file you want to run: ")) - 1
        if 0 <= choice < len(files):
            return files[choice]
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Please enter a valid number.")
        return None

def run_sh_file(file):
    # Run the selected .sh file
    print(f"Running {file}...\n")
    subprocess.run(['bash', file])

def main():
    files = list_sh_files()
    if not files:
        return
    
    display_files(files)
    selected_file = choose_file(files)
    
    if selected_file:
        run_sh_file(selected_file)

if __name__ == "__main__":
    main()
