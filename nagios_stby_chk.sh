#!/bin/sh

: '
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 21/10/2015
Descripcion: BASH script ejecutado en el server de la 
base standby para monitorear la aplicacion de logs. 
Llama a nagios_stby_chk.sql, quien corre la consulta de gap.
'
export ORACLE_SID=SID
export ORACLE_HOME=/oracle/home
export PATH=$ORACLE_HOME/bin:$PATH
export SCRIPT_PATH=/oracle/script

$ORACLE_HOME/bin/sqlplus -s / as sysdba @${SCRIPT_PATH}/sql/nagios_stby_chk.sql
