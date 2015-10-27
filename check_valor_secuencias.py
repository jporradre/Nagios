#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 14/09/2015
Descripcion: Plugin de Nagios para monitorear el valor de secuencias Oracle.
'''


import sys;
import paramiko;

def ayuda():
    msg="check_valor_secuencias : Plugin de Nagios para monitorear el valor de secuencias Oracle.\n. NOTA: El host a monitorear debe tener sqlplus y cargada la clave SSH del server Nagios." \
        "Uso: check_valor_secuencias pHost pSID pBD pServerUser pBDUser pPass pSecs";
    print(msg);


def procesar(pHost,pSID,pBD,pServerUser,pBDUser,pPass,pSecs):
    colSecs = pSecs.split("Ãƒ");
    strres = "OK | ";


    client = paramiko.SSHClient();
    key = paramiko.RSAKey.from_private_key_file("/home/nagios/.ssh/id_rsa");
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy());
    client.connect(pHost, username=pServerUser,pkey = key);

    for sec in colSecs:

        cmd = '. ~/.bash_profile; sqlplus -s '+pBDUser+'/'+pPass+' <<< ''\
                ''"SELECT round(((last_number*100)/ max_value),2) uso  FROM dba_sequences''\
                                      '' WHERE sequence_name =  \''+sec.upper()+'\';"';

        stdin, stdout, stderr = client.exec_command(cmd);

        res = stdout.read() + stderr.read();

        err = res.find("ERROR");

        if err != -1 :
            print("[ERROR] Se encontro un error en la peticion: "+res);
            exit(1);

        if len(res.split("\n")) != 6 :
            print("[ERROR] Cantidad de filas devueltas incorrectas: "+res);
            exit(1);


        strres += (sec + "="+res.split("\n")[3].strip()+";;;; ");

    print(strres);


if len(sys.argv) < 8:
    ayuda();
    exit(1);

procesar(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7]);


