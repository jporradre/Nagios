#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 21/10/2015
Descripcion: Plugin de Nagios para monitorear si la BD Oracle esta levantada.
'''

import socket;
import sys;
import paramiko;


class Check_db_up:
    
    mMaxRein = 1;
    mCantRein = 0;
    
    
    def ayuda(self):
        msg="check_db_up : Plugin de Nagios para monitorear si la BD Oracle esta levantada.\n. NOTA: El host a monitorear debe tener sqlplus y cargada la clave SSH del server Nagios." \
        "Uso: check_db_up   pHost pSID pBD pServerUser pBDUser pBDPass";
        print(msg);


    def procesar(self,pHost,pSID,pBD,pServerUser,pBDUser,pBDPass):
        strres = "OK - Hay conexion con la BD";


        client = paramiko.SSHClient();
        key = paramiko.RSAKey.from_private_key_file("/home/nagios/.ssh/id_rsa");
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy());

        cmd = '. ~/.bash_profile; sqlplus -s '+pBDUser+'/'+pBDPass+' <<< ''\
                ''"SELECT 1 FROM dual;"';

        try:

            client.connect(pHost, port=22, timeout=5, username=pServerUser,pkey = key);
            stdin, stdout, stderr = client.exec_command(cmd);
            res = stdout.read() + stderr.read();

        except socket.timeout:
            if self.mCantRein >= self.mMaxRein:         
                print("La peticion se fue por timeout. Se vuelve a intentar comunicar con el server.");
                exit(1);
            else:
                self.mCantRein += 1;
                self.procesar(pHost,pSID,pBD,pServerUser,pBDUser,pBDPass);


        err = res.find("ERROR");

        if err != -1 :
            print("[ERROR] Se encontro un error en la peticion: "+res);
            exit(1);


        print(strres);
        exit(0);



check = Check_db_up();

if len(sys.argv) == 7:
    check.procesar(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]);
elif len(sys.argv) == 5:
    check.procesar(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],"","");
else:
    ayuda();
    exit(1);


