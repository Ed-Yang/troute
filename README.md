# Python3 traceroute

## Example

```shell
sudo ./troute.py google.com

traceroute to google.com (216.58.200.46), 64 hops max, 24 bytes data
  1  ** - router.asus.com (172.16.1.1) 4 ms 4 ms 4 ms 
  2  TW - h254.s98.ts.hinet.net (168.95.98.254) 7 ms 7 ms 7 ms 
  3  TW - sczs-3312.hinet.net (168.95.23.230) 5 ms 5 ms 5 ms 
  4  TW - tylc-3032.hinet.net (220.128.9.166) 8 ms 8 ms 8 ms 
  5  TW - pcpd-3212.hinet.net (220.128.12.193) 27 ms 
     TW - tyfo-3031.hinet.net (220.128.8.194) 2457 ms 2457 ms 
  6  TW - pcpd-3211.hinet.net (220.128.12.254) 20 ms 
     TW - pcpd-3211.hinet.net (220.128.12.197) 1229 ms 
     TW - pcpd-3211.hinet.net (220.128.12.254) 2706 ms 
  7  US - 72.14.202.178 (72.14.202.178) 7 ms 7 ms 
     US - 72.14.218.140 (72.14.218.140) 1555 ms 
  8  * * * 
  9  US - 209.85.240.14 (209.85.240.14) 65 ms 
     US - 209.85.245.255 (209.85.245.255) 1318 ms 
     US - 209.85.142.12 (209.85.142.12) 2724 ms 
 10  US - 209.85.245.255 (209.85.245.255) 7 ms 
     US - tsa01s08-in-f14.1e100.net (216.58.200.46) 963 ms 963 ms 
```