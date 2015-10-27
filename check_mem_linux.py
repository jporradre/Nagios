#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 26/10/2015
Descripcion: Plugin para Nagios para monitorear el uso de memoria de un host Linux.
'''

import sys;
import paramiko;

def ayuda():
    msg="check_mem_linux : Plugin para Nagios para monitorear el uso de memoria en Linux.\n. NOTA: El host a monitorear debe tener cargada la clave SSH del server Nagios." \
        "Uso: check_mem_linux   pHost pServerUser";
    print(msg);

def procesar(pHost,pServerUser):
    
    head = "";
    strres = "";

    cmd = 'vmstat | tr -s " " | tail -n +2';

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


    fila1 = res.split("\n")[0];
    fila2 = res.split("\n")[1];

    regs1 = fila1.split(" ");
    regs2 = fila2.split(" ");

    regs1.pop(0);
    regs2.pop(0);

    i = 0;

    for reg1 in regs1:
        head += (reg1 + "="+regs2[i]+" ");
        strres += (reg1 + "="+regs2[i]+";;;; ");

        i+=1;


    print(head + " | " + strres);



if len(sys.argv) < 3:
    ayuda();
    exit(1);

procesar(sys.argv[1],sys.argv[2]);
