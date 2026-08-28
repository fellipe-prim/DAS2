import logging
import os
import azure.functions as func
import pyodbc

bp = func.Blueprint()

@bp.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def extract_chamadosla(myTimer: func.TimerRequest) -> None:
    src_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_SOURCE')};DATABASE={os.getenv('SQL_DATABASE_SOURCE')};UID={os.getenv('SQL_USER_SOURCE')};PWD={os.getenv('SQL_PASSWORD_SOURCE')};Encrypt=yes;TrustServerCertificate=no;"
    tgt_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_TARGET')};DATABASE={os.getenv('SQL_DATABASE_TARGET')};UID={os.getenv('SQL_USER_TARGET')};PWD={os.getenv('SQL_PASSWORD_TARGET')};Encrypt=yes;TrustServerCertificate=no;"

    try:
        with pyodbc.connect(src_conn_str) as src_conn:
            cursor_src = src_conn.cursor()
            cursor_src.execute("SELECT id_chamado_sla, id_chamado, id_sla, fl_breach, qt_meta_minutos, dt_referencia FROM itsm.chamado_sla")
            rows = cursor_src.fetchall()

        if rows:
            with pyodbc.connect(tgt_conn_str) as tgt_conn:
                cursor_tgt = tgt_conn.cursor()
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.chamado_sla ON")
                cursor_tgt.execute("DELETE FROM itsm.chamado_sla")
                insert_sql = "INSERT INTO itsm.chamado_sla (id_chamado_sla, id_chamado, id_sla, fl_breach, qt_meta_minutos, dt_referencia) VALUES (?, ?, ?, ?, ?, ?)"
                for row in rows:
                    cursor_tgt.execute(insert_sql, tuple(row))
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.chamado_sla OFF")
                tgt_conn.commit()
                logging.info("Tabela chamado_sla sincronizada.")
    except Exception as e:
        logging.error(f"Erro em chamado_sla: {str(e)}")