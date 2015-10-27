#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 16/10/2015
Descripcion: Plugin de Nagios para monitorear el uso de un dispositivo de almacenamiento de un host Linux mediante IOSTAT.
'''

import sys;
import paramiko;

def ayuda():
    msg="check_iostat : Plugin de Nagios para monitorear el uso de un dispositivo de almacenamiento de un host Linux mediante IOSTAT.\n. NOTA: El host a monitorear debe tener cargada la clave SSH del server Nagios." \
        "Uso: check_iostat   pHost pServerUser pDev";
    print(msg);

def procesar(pHost,pServerUser,pDev):
    headstr = "";
    strres = "OK | ";

    cmd = 'iostat -x -d '+pDev+' | tail -n +3 | head -n +2 | tr -s " "';

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

    head = res.split("\n")[0].split(" ");
    devinfo = res.split("\n")[1].split(" ");
    head.pop(0);
    devinfo.pop(0);
    
    i = 0;
    strres = "";
    
    for headelm in head:
        headstr += headelm + "="+devinfo[i]+" ";  
        strres += (headelm + "="+devinfo[i]+";;;; ");
        i+=1;
        
    print(headstr+" | "+strres);



if len(sys.argv) < 4:
    ayuda();
    exit(1);

procesar(sys.argv[1],sys.argv[2],sys.argv[3]);
