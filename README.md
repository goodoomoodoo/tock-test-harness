# tock-test-harness

## Description

This is a development repository for Tock OS test runner and harness.

## Getting Started

1. Install Ubuntu Server on Raspberry Pi.
    * Follow the guide [here](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#1-overview) until step 5. We do not need desktop environment.
2. Hook up Action Runner of the Tock Repo to the Raspberry Pi.
    * Go to \'Settings\' and go to \'Actions\' down the list on the left
    * Under \'Self-hosted runners\' click **Add runner**
    * Follow the steps to set up action runner on Raspberry Pi
3. Install the [Requirements](https://github.com/tock/tock/blob/master/doc/Getting_Started.md#requirements) here.
4. Install JLinkExe
```bash
$ wget --post-data 'accept_license_agreement=accepted&non_emb_ctr=confirmed&submit=Download+software' https://www.segger.com/downloads/jlink/JLink_Linux_arm64.tgz
$ tar xvf JLink_Linux_arm64.tgz
$ sudo cp JLink_Linux_V700a_arm64/99-jlink.rules /etc/udev/rules.d/ # Depends on JLink version
 
# Add the Jlink directory to the path in .profile or .bashrc
```
5. Checkout test harness in home directory ```cd ~; git clone https://github.com/goodoomoodoo/tock-test-harness.git```

## Troubleshoot

### WiFi not connected after first boot

1. Configure network plan ```sudo vi /etc/netplan/50-cloud-init.yaml```

```yaml
# This file is generated from information provided by the datasource. Changes
# to it will not persist across an instance reboot. To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    ethernets:
        eth0:
            dhcp4: true
            optional: true
    version: 2
    wifis:
        wlan0:
            dhcp4: true
            optional: true
            access-points:
                "SSID_name":
                    password: "WiFi_password"
```
2. Generate and apply new network plan
```sudo netplan generate; sudo netplan apply```
