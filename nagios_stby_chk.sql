/* 
Autor:Juan Pablo Orradre
Fecha ult. modificacion: 21/10/2015
Descripcion: nagios_stby_chk.sql: Script que determina el gap de aplicacion
de logs en la base standby y su criticidad
*/

set linesize 100
set pagesize 0
set feedback OFF
set heading OFF
set newpage NONE

SELECT
  t1.status || ' - Thread: ' || t1.thread# || ', Seq#: ' || t1.sequence# || ', Next time : ' || t1.next_time || ', Gap: ' || t1.gap || ' min ' as "Check"
FROM
  (SELECT
    rownum r,
    b.*
  FROM
    (SELECT
      a.*
    FROM
      (SELECT
        thread#                                           ,
        sequence#                                         ,
        applied                                           ,
        TO_CHAR(next_time, 'dd-mon hh24:mi') "NEXT_TIME",
        CASE
           WHEN(sysdate - next_time) > 1 / 6
           THEN 'CRITICAL'
           ELSE
              CASE
                 WHEN(sysdate - next_time) > 1 / 12
                 THEN 'WARNING'
                 ELSE 'OK'
            END
        END "STATUS",
                ROUND((sysdate - next_time) * 1440) "GAP"
      FROM
        v$archived_log
      WHERE
        applied = 'YES'
      ORDER BY
        sequence# DESC
      ) a
    WHERE
      rownum <= 1
    ORDER BY
      thread#,
      sequence#
    ) b
  ) t1;
EXIT;
