#!/usr/bin/python3
'''
simple switch sample rich.hirata
'''
import logging,signal
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
def get_bridge(driver):
    bridge = Bridge(driver, 'Bridge')
    bridge.add_accessory(SW(driver, 'スウィッチ'))
    return bridge
driver = AccessoryDriver(port=51826, persist_file='home.state')
driver.add_accessory(accessory=get_bridge(driver))
signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()
