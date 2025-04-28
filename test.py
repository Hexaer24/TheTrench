from pprint import pformat
from seleniumbase import SB
with SB(uc=True, headed=True, uc_cdp_events=True) as sb:
    sb.driver.get("https://youtube.com")
    sb.sleep(3)
    sb.driver.add_cdp_listener("Network.responseReceived", lambda data: print(pformat(data)))
    sb.sleep(9999)