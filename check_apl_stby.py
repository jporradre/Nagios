#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 21/10/2015
Descripcion: Plugin de Nagios para monitorear la aplicacion de logs en la base standby.
             NOTA: Referencia al BASH script nagios_stby_chk.sh, subido al repositorio tambien
'''

import sys;
import paramiko;
import socket;

class Check_apl_stby:
    
    mMaxRein = 1;
    mCantRein = 0;
    mPathScript = /path/to/nagios_stby_chk.sh

    def ayuda(self):
        msg="check_apl_stby : Plugin de Nagios para monitorear la aplicacion de logs en la base standby.\n. NOTA: El host a monitorear debe tener cargada la clave SSH del server Nagios." \
        "Uso: check_apl_stby   pHost pServerUser";
        print(msg);

    def procesar(self,pHost,pServerUser):

        cmd = '. '+self.mPathScript;

        client = paramiko.SSHClient();
        key = paramiko.RSAKey.from_private_key_file("/home/nagios/.ssh/id_rsa");
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy());

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
                self.procesar(pHost,pServerUser);
            

        err = res.find("ERROR");

        if err != -1 :
            print("[ERROR] Se encontro un error en la peticion: "+res);
            exit(2);

        err = res.find("CRITICAL");
    
        if err != -1 :
            print(res);
            exit(2);

        err = res.find("WARNING");

        if err != -1 :
            print(res);
            exit(1);

        print(res);
        exit(0);
        

if len(sys.argv) < 3:
    ayuda();
    exit(2);

check = Check_apl_stby();
check.procesar(sys.argv[1],sys.argv[2]);
