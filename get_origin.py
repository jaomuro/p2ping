import ipaddress

def getOriginIP(destIP):
    #conversão da string para um objeto IP
    ipDest = ipaddress.IPv4Address(destIP)

    # obter o endereço de rede do IP de destino fornecido
    network = ipaddress.IPv4Network(ipDest.exploded + '/30', strict=False)

    freeIps = [str(ip) for ip in network.hosts() if ip != ipDest]

    print(freeIps)
    if freeIps:
        return freeIps[0]
    else:
        return None


