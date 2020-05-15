from ubluetooth import BLE, UUID, FLAG_NOTIFY, FLAG_READ, FLAG_WRITE
from micropython import const
from ubinascii import hexlify

IRQ_SCAN_RESULT = const(1 << 4)
IRQ_SCAN_COMPLETE = const(1 << 5)

ADV_TYPES = {
    0x00: "[IND] connectable and scannable undirected advertising",
    0x01: "[DIRECT_IND] connectable directed advertising",
    0x02: "[SCAN_IND] scannable undirected advertising",
    0x03: "[NONCONN_IND] non-connectable undirected advertising",
    0x04: "[SCAN_RSP] scan response"
}

ADV_DATA_TYPES = {
    0x01: "Flags",
    0x02: "Incomplete List of 16-bit Service Class UUIDs",
    0x03: "Complete List of 16-bit Service Class UUIDs",
    0x04: "Incomplete List of 32-bit Service Class UUIDs",
    0x05: "Complete List of 32-bit Service Class UUIDs",
    0x06: "Incomplete List of 128-bit Service Class UUIDs",
    0x07: "Complete List of 128-bit Service Class UUIDs",
    0x08: "Shortened Local Name",
    0x09: "Complete Local Name",
    0x0A: "Tx Power Level",
    0x0D: "Class of Device",
    0x0E: "Simple Pairing Hash C",
    0x0E: "Simple Pairing Hash C-192",
    0x0F: "Simple Pairing Randomizer R",
    0x0F: "Simple Pairing Randomizer R-192",
    0x10: "Device ID",
    0x10: "Security Manager TK Value",
    0x11: "Security Manager Out of Band Flags",
    0x12: "Slave Connection Interval Range",
    0x14: "List of 16-bit Service Solicitation UUIDs",
    0x15: "List of 128-bit Service Solicitation UUIDs",
    0x16: "Service Data",
    0x16: "Service Data - 16-bit UUID",
    0x17: "Public Target Address",
    0x18: "Random Target Address",
    0x19: "Appearance",
    0x1A: "Advertising Interval",
    0x1B: "LE Bluetooth Device Address",
    0x1C: "LE Role",
    0x1D: "Simple Pairing Hash C-256",
    0x1E: "Simple Pairing Randomizer R-256",
    0x1F: "List of 32-bit Service Solicitation UUIDs",
    0x20: "Service Data - 32-bit UUID",
    0x21: "Service Data - 128-bit UUID",
    0x22: "LE Secure Connections Confirmation Value",
    0x23: "LE Secure Connections Random Value",
    0x24: "URI",
    0x25: "Indoor Positioning",
    0x26: "Transport Discovery Data",
    0x27: "LE Supported Features",
    0x28: "Channel Map Update Indication",
    0x29: "PB-ADV",
    0x2A: "Mesh Message",
    0x2B: "Mesh Beacon",
    0x2C: "BIGInfo",
    0x3D: "3D Information Data",
    0xFF: "Manufacturer Specific Data"
}

def dumpAdvData(data):
    i = 0
    while i < len(data):
        advsize = data[i]  # adv_size
        print("[{:02X}]: ".format(data[i+1]), ADV_DATA_TYPES[data[i+1]])
        print("\t", ' '.join('{:02X}'.format(a)
                             for a in data[i+2:i+advsize+1]))
        i += advsize+1

def dump(data):
    return hexlify(data, " ").decode('ascii')

def bt_irq(event, data):
    if event == IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, adv_type, rssi, adv_data = data
        if adv_type in ADV_TYPES:
            print(ADV_TYPES[adv_type])
            print("{addr: ", dump(addr), ", addr_type: ",
                  repr(addr_type), ", rssi:", repr(rssi), "}")
            dumpAdvData(adv_data)
            print("\r\n")

    elif event == IRQ_SCAN_COMPLETE:
        # Scan duration finished or manually stopped.
        print('scan complete')

# Scan continuosly
bt = BLE()
bt.active(True)
bt.irq(handler=bt_irq)
print("Start scanning....", end="")
bt.gap_scan(0, 10, 10)
print("DONE!")
