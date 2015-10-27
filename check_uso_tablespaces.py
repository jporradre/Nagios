#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 26/10/2015
Descripcion: Plugin de Nagios para monitorear el uso de tablespaces Oracle.
'''

import sys;
import paramiko;

def ayuda():
    msg="check_uso_tablespaces : Plugin de Nagios para monitorear el uso de tablespaces Oracle.\n. NOTA: El host a monitorear debe tener sqlplus y cargada la clave SSH del server Nagios." \
        "Uso: check_uso_tablespaces   pHost pSID pBD pServerUser pBDUser pBDPass pTblss";
    print(msg);

def procesar(pHost,pSID,pBD,pServerUser,pBDUser,pBDPass,pTblss):
    colTblss = pTblss.split("Þ");
    head = "";
    strres = "";


    client = paramiko.SSHClient();
    key = paramiko.RSAKey.from_private_key_file("/home/nagios/.ssh/id_rsa");
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy());
    client.connect(pHost, username=pServerUser,pkey = key);

    for tbl in colTblss:

        cmd = '. ~/.bash_profile; sqlplus -s '+pBDUser+'/'+pBDPass+' <<< ''\
                ''"SELECT      ROUND((b.BYTES / a.BYTES) * 100,1) USO'\
                                      '    FROM    (SELECT          TABLESPACE_NAME,          SUM(BYTES) BYTES        FROM          dba_data_files '' \
                                      ''       GROUP BY          TABLESPACE_NAME    ) a,   '' \
                                      ''(      SELECT        TABLESPACE_NAME,        SUM(BYTES) BYTES      FROM        dba_free_space '' \
                                      ''     GROUP BY        TABLESPACE_NAME    ) b    '' \
                                      ''WHERE   a.TABLESPACE_NAME = b.TABLESPACE_NAME  and a.TABLESPACE_NAME = \''+tbl.upper()+'\';"';

        stdin, stdout, stderr = client.exec_command(cmd);

        res = stdout.read() + stderr.read();

        err = res.find("ERROR");

        if err != -1 :
            print("[ERROR] Se encontro un error en la peticion: "+res);
            exit(1);

        if len(res.split("\n")) != 6 :
            print("[ERROR] Cantidad de filas devueltas incorrectas: "+res);
            exit(1);

        head += (tbl + "="+res.split("\n")[3].strip()+"% ");
        strres += (tbl + "="+res.split("\n")[3].strip()+"%;;;; ");

    print(head + " | " + strres);



if len(sys.argv) < 8:
    ayuda();
    exit(1);

procesar(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7]);
