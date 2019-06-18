'''
simple switch 
'''
import broadlink,netaddr,time,binascii,json,sys
import logging,signal
net1={'type': 'SP2', 'ip': '192.168.1.151', 'port': 80, 'mac': '78-0f-77-17-5d-70', 'timeout': 10}
from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import (CATEGORY_SWITCH)
logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")
class SW(Accessory):
     category = CATEGORY_SWITCH
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        serv_tv = self.add_preload_service('Switch')
        self.char_on = serv_tv.configure_char('On', setter_callback=self.sw)
     def sw(self,value):
        logging.info("スウィッチ: %s", value)
        sp2 = broadlink.sp2((net1["ip"], net1["port"]),netaddr.EUI(net1["mac"]),net1["timeout"])
        sp2.auth()
        sp2.set_power(value)
def get_bridge(driver):
    bridge = Bridge(driver, 'Bridge')
    bridge.add_accessory(SW(driver, 'コーヒーメーカ'))
    return bridge
driver = AccessoryDriver(port=51826, persist_file='simple.state')
driver.add_accessory(accessory=get_bridge(driver))
signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()
