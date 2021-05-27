# tock-test-harness

## Description

This is a development repository for Tock OS test runner and harness.

## Getting Started

1. Install Ubuntu Server on Raspberry Pi.
    * Follow the guide [here](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#1-overview) until step 5. We do not need desktop environment.
2. Install the [Requirements](https://github.com/tock/tock/blob/master/doc/Getting_Started.md#requirements) here.
3. Install JLinkExe
```bash
$ wget --post-data 'accept_license_agreement=accepted&non_emb_ctr=confirmed&submit=Download+software' https://www.segger.com/downloads/jlink/JLink_Linux_arm64.tgz
$ tar xvf JLink_Linux_arm64.tgz
$ sudo cp JLink_Linux_V700a_arm64/99-jlink.rules /etc/udev/rules.d/ # Depends on JLink version
 
# Add the Jlink directory to the path in .profile or .bashrc
```

4. Checkout test harness in home directory 
```bash
cd ~; git clone https://github.com/goodoomoodoo/tock-test-harness.git
cd ~; git clone https://github.com/goodoomoodoo/libtock-c.git

```

5. Install gpiozero if not yet installed. (It should come with the image)
```bash
$ sudo pip3 install gpiozero
$ sudo apt install python3-gpiozero
$ sudo chown root:$USER /dev/gpiomem
$ sudo chmod g+rw /dev/gpiomem
```

5. Install linux library
```bash
# Install bluetooth library
$ sudo apt-get install libbluetooth-dev
```

6. Hook up Action Runner of the Tock Repo to the Raspberry Pi.
    * Go to \'Settings\' and go to \'Actions\' down the list on the left
    * Under \'Self-hosted runners\' click **Add runner**
    * Follow the steps to set up action runner on Raspberry Pi

## Troubleshoot
### To run on your local-host (instead of Github)

Make sure to add "self-hosted" as a label in runs-on for the job:

```
jobs:
  "job name":
    runs-on: self-hosted
 ```

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

### Action runner: **command not found**

If you experience issue with the command not being found, but you are very sure that you have installed the corresponding software. Try to uninstall the runner and reinstall it.

```bash
# 1. Uninstall Action Runner Server
$ cd ~/actions-runner
$ sudo ./svc.sh stop
$ sudo ./svc.sh uninstall
$ ./config.sh remove

# 2. Reinstall Action Runner Server
# Follow the guide in Getting Started.
```
**Note**: Possible reason to this issue is that the server environment and path varaible cannot be update after it has started. Thus, it requires a reconfiguration to included the updated path and environment variables.
