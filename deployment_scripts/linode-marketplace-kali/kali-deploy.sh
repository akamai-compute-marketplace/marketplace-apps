#!/bin/bash
## Kali
#<UDF name="kali_everything" label="Would you like to Install the Kali Everything Package?" oneOf="Yes,No" default="Yes">
#<UDF name="kali_headless" label="Would you like to Install the Kali Headless Package?" oneOf="Yes,No" default="No">
#<UDF name="vnc" label="Would you like to setup VNC to access Kali XFCE Desktop" oneOf="Yes,No" default="Yes">
#<UDF name="vnc_username" label="The VNC user to be created for the Linode. The username accepts only lowercase letters, numbers, dashes (-) and underscores (_)">
#<UDF name="vnc_password" label="The password for the limited VNC user">

## Linode/SSH Security Settings
#<UDF name="pubkey" label="The SSH Public Key that will be used to access the Linode" default="">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is required for creating DNS records." default="">
#<UDF name="subdomain" label="The subdomain for the Linode's DNS record (Requires API token)" default="">
#<UDF name="domain" label="The domain for the Linode's DNS record (Requires API token)" default="">
#<UDF name="soa_email_address" label="Email address for SOA records (Requires API token)" default="" >

## Enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1
set -o pipefail

# Source the Linode Bash StackScript, API, and OCA Helper libraries
source <ssinclude StackScriptID=1>
source <ssinclude StackScriptID=632759>
source <ssinclude StackScriptID=401712>

# Source and run the New Linode Setup script for DNS/SSH configuration
source <ssinclude StackScriptID=666912>

function headlessoreverything {
    if [ $HEADLESS == "Yes" ] && [ $EVERYTHING == "Yes" ]; then 
        DEBIAN_FRONTEND=noninteractive apt-get install kali-linux-everything -y -yq -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"
    elif [ $EVERYTHING == "Yes" ] && [ $HEADLESS == "No" ]; then
        DEBIAN_FRONTEND=noninteractive apt-get install kali-linux-everything -y -yq -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"
    elif [ $HEADLESS == "Yes" ] && [ $EVERYTHING == "No" ]; then 
        DEBIAN_FRONTEND=noninteractive apt-get install kali-linux-headless -y -yq -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"
    elif [ $HEADLESS == "No" ] && [ $EVERYTHING == "No" ]; then 
         echo "No Package Selected"
     fi
}

function vncsetup {
    if [ $VNC == "Yes" ]; then 
    ## XFCE & VNC Config
    apt-get install xfce4 xfce4-goodies dbus-x11 tigervnc-standalone-server expect -y -yq -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"

    readonly VNCSERVER_SET_PASSWORD=$(expect -c "
spawn sudo -u $USERNAME vncserver
expect \"Password:\"
send \"$PASSWORD\r\"
expect \"Verify:\"
send \"$PASSWORD\r\"
expect \"Would you like to enter a view-only password (y/n)?\"
send \"n\r\"
expect eof
")
echo "$VNCSERVER_SET_PASSWORD"
    sleep 2
    killvncprocess=$(ps aux | grep "/usr/bin/Xtigervnc :1 -localhost=1 -desktop" | head -n 1 | awk '{ print $2; }')
    kill $killvncprocess
    touch /etc/systemd/system/vncserver@.service
    cat <<EOF > /etc/systemd/system/vncserver@.service
[Unit]
Description=a wrapper to launch an X server for VNC
After=syslog.target network.target
[Service]
Type=forking
User=$USERNAME
Group=$USERNAME
WorkingDirectory=/home/$USERNAME
ExecStartPre=-/usr/bin/vncserver -kill :%i > /dev/null 2>&1
ExecStart=/usr/bin/vncserver -depth 24 -geometry 1280x800 -localhost :%i
ExecStop=/usr/bin/vncserver -kill :%i
[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    systemctl start vncserver@1.service
    systemctl enable vncserver@1.service

    cat <<EOF > /etc/motd
###################################
#   VNC SSH Tunnel Instructions   #
###################################

* Ensure you have a VNC Client installed on your local machine
* Run the command below to start the SSH tunnel for VNC 

    ssh -L 61000:localhost:5901 -N -l $USERNAME $FQDN

* For more Detailed documentation please visit the offical Documentation below

    https://www.linode.com/docs/products/tools/marketplace/guides/kalilinux

### To remove this message, you can edit the /etc/motd file ###
EOF
    fi
}

function main {
    headlessoreverything
    vncsetup
    stackscript_cleanup
}

main