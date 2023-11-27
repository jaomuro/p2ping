#!/usr/bin/env python3

import paramiko
import re
import argparse
import os
from dotenv import load_dotenv
from get_origin import getOriginIP

load_dotenv()
deviceUser = os.getenv('USERNAME')
devicePassword = os.getenv('PASSWORD')

def ssh_and_ping(host, username, password, origin, dest, port=22):
    try:
        # Estabelece uma conexão SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password,port=port)
        try:
                # Executa o comando ping no switch
            ping_command = f'ping -q -a {origin} -m 50 -c 20 {dest}'
            stdin, stdout, stderr = client.exec_command(ping_command)

            # Coleta a saída do comando
            output = stdout.read().decode('utf-8')

            # Analisa as informações do ping
            match = re.search(r'PING.*?([\s\S]*?)<', output)
            if match:
                ping_output = match.group(1).strip()
                print(ping_output)

        except Exception as ping_exception:
            print(f"Erro durante a execução do comando ping: {ping_exception}")

        # Verifica se há mensagens de erro na saída padrão de erro
        error_output = stderr.read().decode('utf-8').strip()
        if error_output:
            print(f"Erro durante a execução do comando ping (stderr): {error_output}")

        # Fecha a conexão SSH
        client.close()

    except paramiko.SSHException as ssh_exception:
        print(f"Erro na conexão SSH: {ssh_exception}")


if __name__ == "__main__":
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Executar ping via SSH em um switch Huawei.')
    parser.add_argument('instance', help='Nome ou IP do switch Huawei')
    # parser.add_argument('origin', help='Endereço de origem para o ping')
    parser.add_argument('destin', help='Endereço de destino para o ping')
    parser.add_argument('--port', type=int, default=22, help='Número da porta SSH (padrão: 22)')

    # Analisa os argumentos da linha de comando
    args = parser.parse_args()

    # Chama a função com os argumentos fornecidos
    originIP = getOriginIP(args.destin)
    ssh_and_ping(args.instance, deviceUser, devicePassword, originIP, args.destin, args.port)
