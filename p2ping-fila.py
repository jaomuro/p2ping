#!/usr/bin/env python3

import paramiko
import re
import argparse
import os
from dotenv import load_dotenv
from get_origins import getOriginsIP
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
deviceUser = os.getenv('USERNAME')
devicePassword = os.getenv('PASSWORD')

def ssh_and_ping_worker(host, username, password, origin, dest, port=22):
    try:
        # Estabelece uma conexão SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password, port=port)


        # Executa o comando ping no switch
        ping_command = f'ping -q -a {origin} -m 50 -c 20 {dest}'
        stdin, stdout, stderr = client.exec_command(ping_command)

        try:
            # Coleta a saída do comando
            output = stdout.read().decode('utf-8')

            # Analisa as informações do ping
            match = re.search(r'PING.*?([\s\S]*?)<', output)
            if match:
                ping_output = match.group(1).strip()
                print(ping_output)

        except Exception as ping_exception:
            print(f"Erro durante a execução do comando ping: {ping_exception}")
            print("Saída de erro detalhada:")
            print(stderr.read().decode('utf-8'))

            client.close()

    except paramiko.SSHException as ssh_exception:
        print(f"Erro na conexão SSH: {ssh_exception}")

def ssh_and_ping(host, username, password, origins, destins, port=22):
    with ThreadPoolExecutor(max_workers=len(origins)) as executor:
        # Usa ThreadPoolExecutor para executar os testes de ping em paralelo
        futures = [
            executor.submit(ssh_and_ping_worker, host, username, password, origin, dest, port)
            for origin, dest in zip(origins, destins)
        ]

        # Aguarda a conclusão de todas as threads
        for future in futures:
            future.result()

if __name__ == "__main__":
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Executar ping via SSH em um switch Huawei.')
    parser.add_argument('instance', help='Nome ou IP do switch Huawei')
    parser.add_argument('destin', nargs='+', help='Endereço de destino para o ping')
    parser.add_argument('--port', type=int, default=22, help='Número da porta SSH (padrão: 22)')

    # Analisa os argumentos da linha de comando
    args = parser.parse_args()

    # Obtém a lista de IPs de origem
    originIPs = getOriginsIP(args.destin)

    # Chama a função com os argumentos fornecidos
    ssh_and_ping(args.instance, deviceUser, devicePassword, originIPs, args.destin, args.port)
