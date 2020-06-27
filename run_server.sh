#!/bin/sh
#

echo "Creating directories..."
mkdir -p db/Registry
mkdir -p IceStorm/ 

echo "Exec registry"
icegridregistry --Ice.Config=registry.config &
sleep 1

echo "Exec icestorm"
icebox --Ice.Config = icebox.config &
sleep 1

./sender_factory.py --Ice.Config=senders.config files/ &
sleep 1
./transfers_manager.py --Ice.Config=transfers.config

echo "Shoutting down..."
sleep 1
rm $OUT
