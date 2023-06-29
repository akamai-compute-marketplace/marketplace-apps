#!/bin/bash
#<UDF name="PORT" Label="MC2GO P2 AVC Ultra Transcoder Port" example="Default: 8080" default="8080" />

## Enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

# Apt update/upgrade
apt update
apt -y upgrade

# Install the dependencies & add Docker to the APT repository
apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg2 pwgen ufw
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

# Update & install Docker-CE
apt update
apt install -y docker-ce

# Check to ensure Docker is running and installed correctly
systemctl status docker
docker -v

# Run
docker run -d \
    --name mc2gop2avc \
    -e ACCEPT_EULA=y \
    -e TAAS_PARAMS=verbosity=FULL \
    -e TAAS_SERVER= \
    -e TAAS_VERBOSITY=FULL \
    -e TAAS_CID= \
    -e AUTOSTART=true \
    -e JOBS= \
    -p $PORT:8080 \
    mainconcept/mc_2go_p2_avc_ultra_transcoder:demo-2-3-621

echo "
********************************************************************************
Welcome to MainConcept 2GO P2 AVC Ultra Transcoder!
********************************************************************************
  # MC2GO Access:           http://$IP:$PORT/
  # Website:                https://www.mainconcept.com/mc2go
  # Documentation:          https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%202GO%20-%20P2%20AVC%20Ultra%20Transcoder.pdf?hsLang=en
  # Rest API Documentation: https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%202GO%20-%20REST%20API.pdf?hsLang=en  
"