import logging
import os
import azure.functions as func
import pyodbc

bp = func.Blueprint()

@bp.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def extract_fila(myTimer: func.TimerRequest) -> None:
    logging.info('Sincronizando: fila')
    
    src_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_SOURCE')};DATABASE={os.getenv('SQL_DATABASE_SOURCE')};UID={os.getenv('SQL_USER_SOURCE')};PWD={os.getenv('SQL_PASSWORD_SOURCE')};Encrypt=yes;TrustServerCertificate=no;"
    tgt_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_TARGET')};DATABASE={os.getenv('SQL_DATABASE_TARGET')};UID={os.getenv('SQL_USER_TARGET')};PWD={os.getenv('SQL_PASSWORD_TARGET')};Encrypt=yes;TrustServerCertificate=no;"

    try:
        with pyodbc.connect(src_conn_str) as src_conn:
            cursor_src = src_conn.cursor()
            cursor_src.execute("SELECT id_fila, cd_fila, nm_fila, ds_descricao, fl_ativo FROM itsm.fila")
            rows = cursor_src.fetchall()

        if rows:
            with pyodbc.connect(tgt_conn_str) as tgt_conn:
                cursor_tgt = tgt_conn.cursor()
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.fila ON")
                cursor_tgt.execute("DELETE FROM itsm.fila")
                
                insert_sql = "INSERT INTO itsm.fila (id_fila, cd_fila, nm_fila, ds_descricao, fl_ativo) VALUES (?, ?, ?, ?, ?)"
                for row in rows:
                    cursor_tgt.execute(insert_sql, tuple(row))
                
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.fila OFF")
                tgt_conn.commit()
    except Exception as e:
        logging.error(f"Erro em fila: {str(e)}")