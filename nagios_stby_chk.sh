#!/bin/sh
export ORACLE_SID=SID
export ORACLE_HOME=/oracle/home
export PATH=$ORACLE_HOME/bin:$PATH
export SCRIPT_PATH=/oracle/script

$ORACLE_HOME/bin/sqlplus -s / as sysdba @${SCRIPT_PATH}/sql/nagios_stby_chk.sql
