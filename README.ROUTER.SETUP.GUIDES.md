# Router Setup Guides
These guides assume that the Arris NTD is listening on `192.168.0.1/24` therefor if you find that your Arris is not able to be connected to post a factory reset then I would suggesting trying `192.168.100.1/24`.

The following devices appear to sort it out automatically:
  * Asus AC68/58 series
  * Google Wifi

## Ubiquiti Edge & USG Products
As an UBNT user, the below should gain you access assuming NBN has not disabled access. Has been tested on Edgerouter and USG products.
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

## Openwrt
Placeholder

## Pfsense
Placeholder
