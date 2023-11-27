import ipaddress

def getOriginsIP(dest_ips):
    origin_ips = []

    for dest_ip in dest_ips:
        # Conversão da string para um objeto IP
        ipDest = ipaddress.IPv4Address(dest_ip)

        # Obter o endereço de rede do IP de destino fornecido
        network = ipaddress.IPv4Network(ipDest.exploded + '/30', strict=False)

        freeIps = [str(ip) for ip in network.hosts() if ip != ipDest]

        if freeIps:
            origin_ips.append(freeIps[0])
        else:
            origin_ips.append(None)
    print(origin_ips)
    return origin_ips


