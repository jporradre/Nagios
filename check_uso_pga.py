#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 26/10/2015
Descripcion: Plugin de Nagios para monitorear el uso de memoria PGA por proceso en Oracle.
'''

import sys;
import paramiko;

def ayuda():
    msg="qcheck_uso_pga : Plugin de Nagios para monitorear el uso de memoria PGA por proceso en Oracle.\n. NOTA: El host a monitorear debe tener cargada la clave SSH del server Nagios." \
        "Uso: qcheck_uso_pga   pHost pSID pBD pServerUser pBDUser pBDPass";
    print(msg);

def procesar(pHost,pSID,pBD,pServerUser,pBDUser,pBDPass):

    strres = "";

    cmd = '. ~/.bash_profile; sqlplus -s '+pBDUser+'/'+pBDPass+' as sysdba <<< ''\
                ''"SELECT ROUND(SUM(pga_used_mem)/(1024*1024),2) PGA_USED_MB FROM v\$process;"';


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

    strres += (res.split("\n")[1] + "="+res.split("\n")[3].strip()+"MB;;;; ");

    print(res.split("\n")[1] + "="+res.split("\n")[3].strip()+"MB | " +strres);



if len(sys.argv) == 7:
    procesar(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]);
elif len(sys.argv) == 5:
    procesar(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],"","");
else:
    ayuda();
    exit(1);
