#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 26/10/2015
Descripcion: Plugin de Nagios para monitorear la cantidad de objetos invÃ¡lidos Oracle.
'''

import sys;
import paramiko;

def ayuda():
    msg="check_objs_invs : Plugin para Nagios para monitorear la cantidad de objetos invÃ¡lidos Oracle mediante sqlplus.\n. NOTA: El host a monitorear debe tener cargada la clave SSH del server Nagios." \
        "Uso: check_objs_invs   pHost pSID pBD pServerUser pBDUser pBDPass";
    print(msg);

def procesar(pHost,pSID,pBD,pServerUser,pBDUser,pBDPass):

    strres = "";
    head = "";

    cmd = '. ~/.bash_profile; sqlplus -s '+pBDUser+'/'+pBDPass+' as sysdba <<< ''\
                ''"SELECT  count(*) FROM dba_objects WHERE STATUS =\'INVALID\';"';


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

    if int(res.split("\n")[3].strip()) > 0:

        cmd = '. ~/.bash_profile; sqlplus -s '+pBDUser+'/'+pBDPass+' <<< ''\
                ''"SELECT  owner || \'|\' || count(*) FROM dba_objects WHERE STATUS =\'INVALID\' GROUP BY owner ORDER BY owner;"';


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

        i = 0;

        for line in res.split("\n"):
            if (i > 2 and line.strip() != ""):
                head += line.split("|")[0] + "="+line.split("|")[1] + " ";
                strres += (line.split("|")[0] + "="+line.split("|")[1] +";;;; ");

            i += 1;


    print(head+" | "+strres);



if len(sys.argv) < 7:
    ayuda();
    exit(1);

procesar(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]);
