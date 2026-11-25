#!/usr/bin/env python3
"""subnet_toolkit.py - a small, dependency-free subnet and CIDR helper.

Commands:
  info      <cidr>                 Show details for one network
  check     <ip> <cidr>            Is an IP inside a network?
  summarize <cidr> [cidr ...]      Collapse a list of networks into the
                                   smallest possible set of CIDRs

Examples:
  python3 subnet_toolkit.py info 192.168.1.0/24
  python3 subnet_toolkit.py check 192.168.1.10 192.168.1.0/24
  python3 subnet_toolkit.py summarize 192.168.0.0/24 192.168.1.0/24
"""

import ipaddress
import sys


def cmd_info(args):
    if len(args) != 1:
        raise SystemExit("usage: info <cidr>")
    net = ipaddress.ip_network(args[0], strict=False)
    hosts = list(net.hosts())
    print(f"Network:        {net.network_address}")
    print(f"Broadcast:      {net.broadcast_address}")
    print(f"Netmask:        {net.netmask}")
    print(f"Wildcard mask:  {net.hostmask}")
    print(f"Prefix length:  /{net.prefixlen}")
    print(f"Total addresses:{net.num_addresses:>12,}")
    print(f"Usable hosts:   {len(hosts):,}")
    if hosts:
        print(f"First usable:   {hosts[0]}")
        print(f"Last usable:    {hosts[-1]}")
    print(f"Private:        {net.is_private}")
    return 0


def cmd_check(args):
    if len(args) != 2:
        raise SystemExit("usage: check <ip> <cidr>")
    ip = ipaddress.ip_address(args[0])
    net = ipaddress.ip_network(args[1], strict=False)
    inside = ip in net
    print(f"{ip} is {'INSIDE' if inside else 'NOT inside'} {net}")
    return 0 if inside else 1


def cmd_summarize(args):
    if not args:
        raise SystemExit("usage: summarize <cidr> [cidr ...]")
    nets = [ipaddress.ip_network(a, strict=False) for a in args]
    v4 = [n for n in nets if n.version == 4]
    v6 = [n for n in nets if n.version == 6]
    result = []
    if v4:
        result += list(ipaddress.collapse_addresses(v4))
    if v6:
        result += list(ipaddress.collapse_addresses(v6))
    print(f"{len(nets)} network(s) summarized into {len(result)}:")
    for n in result:
        print(f"  {n}")
    return 0


COMMANDS = {"info": cmd_info, "check": cmd_check, "summarize": cmd_summarize}


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd = COMMANDS.get(argv[1])
    if cmd is None:
        print(f"unknown command: {argv[1]}\n")
        print(__doc__)
        return 2
    try:
        return cmd(argv[2:])
    except ValueError as exc:
        print(f"error: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
