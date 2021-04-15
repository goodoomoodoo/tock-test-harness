# tock-test-harness

## Description

This is a development repository for Tock OS test runner and harness.

## Getting Started

1. Install Ubuntu Server on Raspberry Pi.
    * Follow the guide [here](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#1-overview) until step 5. We do not need desktop environment.
2. Follow Tock OS [Getting Started](https://github.com/goodoomoodoo/tock/blob/master/doc/Getting_Started.md) Guide.

## Troubleshoot

### WiFi not connected after first boot

1. Configure network plan
```sudo vi /etc/netplan/50-cloud-init.yaml```
```
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
