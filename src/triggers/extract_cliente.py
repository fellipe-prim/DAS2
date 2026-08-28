import logging
import os
import azure.functions as func
import pyodbc

bp = func.Blueprint()

@bp.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def extract_cliente(myTimer: func.TimerRequest) -> None:
    logging.info('Sincronizando: cliente_organizacao')
    
    src_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_SOURCE')};DATABASE={os.getenv('SQL_DATABASE_SOURCE')};UID={os.getenv('SQL_USER_SOURCE')};PWD={os.getenv('SQL_PASSWORD_SOURCE')};Encrypt=yes;TrustServerCertificate=no;"
    tgt_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_TARGET')};DATABASE={os.getenv('SQL_DATABASE_TARGET')};UID={os.getenv('SQL_USER_TARGET')};PWD={os.getenv('SQL_PASSWORD_TARGET')};Encrypt=yes;TrustServerCertificate=no;"

    try:
        with pyodbc.connect(src_conn_str) as src_conn:
            cursor_src = src_conn.cursor()
            cursor_src.execute("SELECT id_cliente_organizacao, cd_cliente_organizacao, nm_cliente_organizacao, nr_cnpj, fl_ativo FROM itsm.cliente_organizacao")
            rows = cursor_src.fetchall()

        if rows:
            with pyodbc.connect(tgt_conn_str) as tgt_conn:
                cursor_tgt = tgt_conn.cursor()
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.cliente_organizacao ON")
                cursor_tgt.execute("DELETE FROM itsm.cliente_organizacao")
                
                insert_sql = "INSERT INTO itsm.cliente_organizacao (id_cliente_organizacao, cd_cliente_organizacao, nm_cliente_organizacao, nr_cnpj, fl_ativo) VALUES (?, ?, ?, ?, ?)"
                for row in rows:
                    cursor_tgt.execute(insert_sql, tuple(row))
                
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.cliente_organizacao OFF")
                tgt_conn.commit()
    except Exception as e:
        logging.error(f"Erro em cliente: {str(e)}")