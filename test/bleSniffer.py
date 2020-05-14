from ubluetooth import BLE, UUID, FLAG_NOTIFY, FLAG_READ, FLAG_WRITE
from micropython import const
from ubinascii import hexlify

IRQ_SCAN_RESULT                     = const(1 << 4)
IRQ_SCAN_COMPLETE                   = const(1 << 5)

ADV_TYPES = { 0x00: "[IND] connectable and scannable undirected advertising",
              0x01: "[DIRECT_IND] connectable directed advertising",
              0x02: "[SCAN_IND] scannable undirected advertising",
              0x03: "[NONCONN_IND] non-connectable undirected advertising",
              0x04: "[SCAN_RSP] scan response"}

def dump(data):
    return hexlify(data, " ").decode('ascii')

def bt_irq(event, data):
    if event == IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, adv_type, rssi, adv_data = data
        if adv_type in ADV_TYPES:
            print(ADV_TYPES[adv_type])
            print("{ addr_type: ", repr(addr_type), ", rssi:", repr(rssi), ",")
            print("addr: ", dump(addr), ", adv_data: ", dump(adv_data),"}")
    elif event == IRQ_SCAN_COMPLETE:
        # Scan duration finished or manually stopped.
        print('scan complete')

# Scan continuosly
bt = BLE()
bt.active(True)
bt.irq(handler=bt_irq)
print("Start scanning....", end="")
bt.gap_scan(0,10,10)
print("DONE!")