# Router Setup Guides
## Ubiquiti Edge & USG Products
As an UBNT user, the below should gain you access assuming NBN has not disabled access. Has been tested on Edgerouter and USG products.

Note: Your Arris may also be setup to listen on 192.168.100.1/24 so modifying the below `peth0 address` would be required.
```bash
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
