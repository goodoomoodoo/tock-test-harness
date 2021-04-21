#!/bin/bash
# RPi Test Runner

# Change directory to the nrf52840 development kit directory
cd ~/actions-runner/_work/tock/tock/boards/nordic/nrf52840dk/

# Compile
make

# Install bin
make install

# Install Blink App
tockloader install --board nrf52dk --jlink blink < '1'
