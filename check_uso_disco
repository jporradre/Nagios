#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 26/10/2015
Descripcion: Plugin de Nagios para monitorear el uso de disco de un host Linux.
'''

import sys;
import paramiko;

def ayuda():
    msg="check_uso_disco : Plugin de Nagios para monitorear el uso de disco de un host Linux.\n. NOTA: El host a monitorear debe tener cargada la clave SSH del server Nagios." \
        "Uso: check_uso_disco   pHost pServerUser";
    print(msg);

def procesar(pHost,pServerUser):

    head = "";
    strres = "";

    cmd = 'df -Ph | tr -s " " | cut -d " " -f 5,6  | tail -n +2';

    client = paramiko.SSHClient();
    key = paramiko.RSAKey.from_private_key_file("/home/nagios/.ssh/id_rsa");
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy());
    client.connect(pHost, username=pServerUser,pkey = key);

    stdin, stdout, stderr = client.exec_command(cmd);

    res = stdout.read() + stderr.read();

    err = res.find("ERROR");

    if err != -1 :
        print("[ERROR] Se encontro un error en la peticion: "+res);
        exit(1);

    dirsDU = res.split("\n");

    for dirDU in dirsDU:
        if dirDU != "":
            head += (dirDU.split(" ")[1] + "="+dirDU.split(" ")[0]+" ");
            strres += (dirDU.split(" ")[1] + "="+dirDU.split(" ")[0]+";;;; ");

    print(head + " | " +strres);



if len(sys.argv) < 3:
    ayuda();
    exit(1);

procesar(sys.argv[1],sys.argv[2]);
