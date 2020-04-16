# Router Setup Guides
These guides assume that the Arris NTD is listening on `192.168.0.1/24` therefor if you find that your Arris is not able to be connected to post a factory reset then I would suggesting trying `192.168.100.1/24`.

The following devices appear to sort it out automatically:
  * Asus AC68/58 series
  * Google Wifi

## Ubiquiti [EdgeMAX](https://www.ui.com/products/#edgemax) & [Unifi USG](https://www.ui.com/products/#unifi) Products
As an UBNT user, the below should gain you access assuming NBN has not disabled access. Has been tested on Edgerouter and Unifi USG hardware.
```
@Edge:~$ configure
[edit]
@Edge#

set interfaces pseudo-ethernet peth0 address 192.168.0.2/24
set interfaces pseudo-ethernet peth0 description 'Modem Access'
set interfaces pseudo-ethernet peth0 link eth0
commit
set service nat rule 5000 description 'masquerade for HFC Modem'
set service nat rule 5000 outbound-interface peth0
set service nat rule 5000 type masquerade
commit
save
```
Once this has been completed, committed and saved the following command should return something very similar to the below. (if your WAN is not eth0 then please change accordingly)
```
@Edge:~# arp -a | grep eth0
? (192.168.0.1) at xx:xx:xx:xx:xx:xx [ether] on peth0
loop180150120.bng1.vdc01.syd.aussiebb.net (180.150.12.1) at 00:a2:00:b2:00:c2 [ether] on eth0
```

## [Pfsense](https://www.pfsense.org/)
### Summary
Identify the ethernet interface that the NBN NTD is physically connected to. Check its configuration: Is the WAN working through it directly (Eg. over IPoA)? If so, it is probably set to obtain an IP address via DHCP. However maybe it uses something like PPPoE to establish a higher level link. Either way, to route data to the NTD's admin interface, you will need to define another interface (physical or virtual), and assign it a suitable name, a non-routable IP address and subnet.

###### Note
*If you already have a LAN or OPT interface defined with the subnet 192.168.0.x, your router will not allow a duplicate network. Consider changing your LAN or OPT interface subnet to something else, such as to 192.168.y.x where y=2-254 (y may not be 0)*

### Steps
1. Check the list of available interfaces for the one that connects to the NTD. If it was already created, enable it and/or check its configuration is correct, by completing the steps below). Alternately, if your BSD router connects via IPoA, the interface will already be enabled and configured to use DHCP. It receives a routable IP address from your ISP which your NTD and BSD router maintain over this interface, so you must create a virtual (VLAN) interface instead. Then:
2. Assign the IP address 192.168.0.254 (anything 192.168.0.2-254 can work)
3. Assign the subnet (eg. /24 or 255.255.255.0)
4. Apply
5. Check, update or create the necessary LAN firewall rules to allow traffic from your laptop/desktop PC to the TCP ports on the new subnet (80, 8080, etc.)
6. Check you can hit http://192.168.0.1/cmconnectionstatus.html with your browser

###### Note
*Some modems may connect to 192.168.100.1 so please make the appropriate changes where necessary.*

Thanks to [W. Pooler](https://forums.whirlpool.net.au/user/58958 "W. Pooler") for this writeup.

## [OpenWRT](https://openwrt.org)
In a relatively typical environment the below should work, naturally this won't be perfect for everyone.
```bash
uci set network.CM_ACCESS=interface
uci set network.CM_ACCESS.proto='static'
uci set network.CM_ACCESS.ifname='eth0.2'
uci set network.CM_ACCESS.ipaddr='192.168.0.2'
uci set network.CM_ACCESS.netmask='255.255.255.0'
uci commit
/etc/init.d/network restart
```
Remember to replace `CM_ACCESS` with the name of interface you wish to name it as, `eth0.2` with the actual interface of your "WAN" which should begin with the words `eth` not `wan` for example. Alternatively, there is a [LuCI/webUI guide](https://simplebeian.wordpress.com/2014/03/12/accessing-your-modem-from-openwrt-router/), should you prefer to go through that route.

## [MikroTik](https://mikrotik.com/)
This is assuming 'ether1' is your NBN modem uplink, simply login via SSH or telnet, and attach the IP to ether1:

```bash
[admin@MikroTik] > ip address add address=192.168.0.2/24 interface=ether1 network=192.168.0.0
```

Confirm it works via ping (or `ip address print`):
```bash
[admin@MikroTik] > ping 192.168.0.1 count=5
  SEQ HOST                                     SIZE TTL TIME  STATUS
    0 192.168.0.1                                56  64 3ms
    1 192.168.0.1                                56  64 3ms
    2 192.168.0.1                                56  64 3ms
    3 192.168.0.1                                56  64 3ms
    4 192.168.0.1                                56  64 3ms
    sent=5 received=5 packet-loss=0% min-rtt=3ms avg-rtt=3ms max-rtt=3ms
```

Thanks to [net-wayfarer](https://github.com/net-wayfarer) for this writeup.
