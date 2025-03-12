#air-connector

import asyncio
import time
import pyatv
from pyatv.const import Protocol
from . import log
import pyatv.storage.file_storage as pfs
log.setLevel(log.DEBUG)
import easygui

async def pair(airplayDevice, loop):
    #atvs = await pyatv.scan(loop)
    log.debug(airplayDevice)
    log.debug(Protocol.AirPlay)
    pairing = await pyatv.pair(airplayDevice, Protocol.AirPlay, loop)
    await pairing.begin()
    #log.debug("pairingHandler: ", pairing)

    if pairing.device_provides_pin:
        #pin = int(input("Enter PIN: "))
        log.debug("This device has a PIN.")
        #pin = int(await asyncio.to_thread(input, "Enter PIN:"))
        pin = easygui.enterbox("What is PIN for this device??")
        #pairing.pin(pin)
    else:
        #pairing.pin(1234)  # Should be randomized
        log.debug("This device has no PIN.")
        #input("Enter this PIN on the device: 1234")
        log.debug("idk")
    
    #pin = int(3005)
    
    
    print(pin)
    pairing.pin(pin)
    await pairing.finish()
    print("Pairing.finished")
    stor = pfs.FileStorage("pyatv.conf", loop)
    # Give some feedback about the process
    if pairing.has_paired:
        print("Paired with device!")
        print("Credentials:", pairing.service.credentials)
        psc = pairing.service.credentials
        airplayDevice.get_service(Protocol.AirPlay).credentials = pairing.service.credentials
        airplayDevice.set_credentials(Protocol.AirPlay, psc)
        #print(conf, "\n\n", type(conf))
        await stor.update_settings(airplayDevice)
        print("\n\nPAIRED DEVICE----------------\n", airplayDevice, "\n\n", type(airplayDevice))
    else:
        print("Did not pair with device!")
    
    
    await pairing.close()
    return airplayDevice

async def connect_to_device(ip):
    #loop = asyncio.get_event_loop()
    loop = asyncio.get_event_loop()
    atvs = await pyatv.scan(loop)
    for atv in atvs:
        print(str(atv.address))
        if str(atv.address) == ip:
            print(f"Found  {atv.name}...")
            print("atv.services:")
            print(atv.services[1])
            print(atv.services)
            print(f"Pairing to  {atv.name}...")
            tv_w_password = await pair(atv, loop)
            #time.sleep(3000)
            try:
                apple_tv = await pyatv.connect(tv_w_password, loop)
            except Exception  as e:
                log.error(f"ERROR connecting to {atv.name}. error was {e}")
                return -1
            return apple_tv
        else:
            continue
            #print(f"The address  was {atv.address}, ip was {ip}. \nTypeof  address: {type(atv.address)}. Typeof  ip: {type(ip)}.")
    print("Device not found")

# Replace with the IP address of your AirPlay device
#device_ip = "192.168.1.100"

#asyncio.run(connect_to_device(device_ip))
