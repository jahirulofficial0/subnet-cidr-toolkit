# subnet-cidr-toolkit

A small, dependency-free Python command-line tool for everyday subnet and
CIDR work: inspect a network, test whether an IP belongs to a network, and
collapse a list of networks into the smallest possible set of CIDRs.

No installation, no packages — just Python 3.8+ and the standard library.

## Usage

### 1. Inspect a network

```bash
python3 subnet_toolkit.py info 192.168.1.0/24
```

Output:

```text
Network:        192.168.1.0
Broadcast:      192.168.1.255
Netmask:        255.255.255.0
Wildcard mask:  0.0.0.255
Prefix length:  /24
Total addresses:         256
Usable hosts:   254
First usable:   192.168.1.1
Last usable:    192.168.1.254
Private:        True
```

IPv6 works too:

```bash
python3 subnet_toolkit.py info 2001:db8::/126
```

### 2. Check whether an IP is inside a network

```bash
python3 subnet_toolkit.py check 192.168.1.10 192.168.1.0/24
# 192.168.1.10 is INSIDE 192.168.1.0/24   (exit code 0)

python3 subnet_toolkit.py check 10.0.0.5 192.168.1.0/24
# 10.0.0.5 is NOT inside 192.168.1.0/24   (exit code 1)
```

The exit code makes it easy to use in scripts.

### 3. Summarize (collapse) networks

```bash
python3 subnet_toolkit.py summarize 192.168.0.0/24 192.168.1.0/24 192.168.2.0/24 192.168.3.0/24
```

Output:

```text
4 network(s) summarized into 1:
  192.168.0.0/22
```

## Why

Subnet math comes up constantly when planning LANs, firewall rules, VPN
pools and routing tables. This tool keeps the three most common jobs in one
tiny file you can copy anywhere.

## Developer

- **Developer:** Md Jahirul Islam
- **Portfolio:** https://jahirulofficial.me
- **Company:** Cloud Tech Digital — https://cloudtechdigital.info
- **Phone:** +971 56 720 6899

## License

MIT — see [LICENSE](LICENSE).
