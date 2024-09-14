#!/bin/bash

# Function to print messages
ui_print() {
    echo -e "\n$1\n"
}

# Check if Wine is installed
if ! command -v wine &> /dev/null; then
    ui_print "Wine is not installed. Installing Wine..."
    sudo dpkg --add-architecture i386
    sudo apt update
    sudo apt install wine64 wine32 -y
else
    ui_print "Wine is already installed."
fi

# Install useful dependencies for Wine
ui_print "Installing dependencies for better .exe support..."
sudo apt install -y winetricks p7zip-full p7zip-rar lib32gcc-s1 libfaudio0:i386

# Setting Wine to 64-bit (if your system is 64-bit)
if [ "$(getconf LONG_BIT)" = "64" ]; then
    ui_print "Setting Wine to 64-bit mode..."
    WINEPREFIX=~/.wine WINEARCH=win64 winecfg
fi

# Configure Wine for performance
ui_print "Configuring Wine for better performance..."
winetricks settings dxvk
winetricks settings csmt=on
winetricks settings vcrun2015

# Cleaning up Wine cache and temporary files
ui_print "Cleaning up Wine temporary files..."
rm -rf ~/.wine/drive_c/windows/temp/*
rm -rf ~/.wine/drive_c/users/$USER/Temp/*

# Optimize your system for Wine by disabling unnecessary services
ui_print "Disabling unnecessary services to improve performance..."
sudo systemctl disable bluetooth
sudo systemctl disable cups-browsed

# Enabling performance optimizations
ui_print "Enabling system optimizations for Wine..."
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
echo "vm.vfs_cache_pressure=50" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Creating a script for regular Wine cleanup
ui_print "Creating a Wine cleanup script..."
cat <<EOF > ~/wine_cleanup.sh
#!/bin/bash
rm -rf ~/.wine/drive_c/windows/temp/*
rm -rf ~/.wine/drive_c/users/\$USER/Temp/*
echo "Wine cache and temp files cleaned."
EOF

chmod +x ~/wine_cleanup.sh

ui_print "Setup complete. Your system is now optimized for running .exe files through Wine."
ui_print "You can use ~/wine_cleanup.sh to regularly clean Wine temp files."
