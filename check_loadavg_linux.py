#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 04/11/2015
Descripcion: Plugin para Nagios para monitorear el load average de un host Linux.
'''

import sys;
import paramiko;

def ayuda():
    msg="check_loadavg_linux : Plugin para Nagios para monitorear el load average de un host Linux.\n. NOTA: El host a monitorear debe tener cargada la clave SSH del server Nagios." \
        "Uso: check_loadavg_linux   pHost pServerUser";
    print(msg);

def procesar(pHost,pServerUser):

    strres = "";
	
    cmd = 'top -n 1 -b | head -n 1 | sed "s/^.*load average: //g" | tr -s "," " " ; cat /proc/cpuinfo | grep processor | wc -l';

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


    loads = res.split("\n")[0].split(" ");
    cantCores = int(res.split("\n")[1].strip());
	
    u1m = "u1min="+loads[0];
    u5m = "u5min="+loads[1];
    u15m = "u15min="+loads[2];

    strres += (u1m+' '+u5m+' '+u15m+' | '+u1m+";;;; "+u5m+";"+str(cantCores)+";"+str(cantCores+(cantCores/2))+";; "+u15m+";"+str(cantCores)+";"+str(cantCores+(cantCores/2))+";; ");
    
    print(strres);


if len(sys.argv) < 3:
    ayuda();
    exit(1);

procesar(sys.argv[1],sys.argv[2]);
