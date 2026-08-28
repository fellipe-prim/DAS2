import logging
import os
import azure.functions as func
import pyodbc

bp = func.Blueprint()

@bp.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def extract_chamado(myTimer: func.TimerRequest) -> None:
    src_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_SOURCE')};DATABASE={os.getenv('SQL_DATABASE_SOURCE')};UID={os.getenv('SQL_USER_SOURCE')};PWD={os.getenv('SQL_PASSWORD_SOURCE')};Encrypt=yes;TrustServerCertificate=no;"
    tgt_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_TARGET')};DATABASE={os.getenv('SQL_DATABASE_TARGET')};UID={os.getenv('SQL_USER_TARGET')};PWD={os.getenv('SQL_PASSWORD_TARGET')};Encrypt=yes;TrustServerCertificate=no;"

    try:
        with pyodbc.connect(src_conn_str) as src_conn:
            cursor_src = src_conn.cursor()
            cursor_src.execute("""
                SELECT id_chamado, nr_chamado, ds_tipo_chamado, ds_status_chamado, ds_prioridade, 
                       dt_criacao, dt_resolucao, dt_ultima_atualizacao, id_analista_atual, 
                       id_reporter, id_categoria, id_cliente_organizacao, id_fila_atual, ds_titulo 
                FROM itsm.chamado
            """)
            rows = cursor_src.fetchall()

        if rows:
            with pyodbc.connect(tgt_conn_str) as tgt_conn:
                cursor_tgt = tgt_conn.cursor()
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.chamado ON")
                cursor_tgt.execute("DELETE FROM itsm.chamado")
                insert_sql = """
                    INSERT INTO itsm.chamado (id_chamado, nr_chamado, ds_tipo_chamado, ds_status_chamado, ds_prioridade, 
                                            dt_criacao, dt_resolucao, dt_ultima_atualizacao, id_analista_atual, 
                                            id_reporter, id_categoria, id_cliente_organizacao, id_fila_atual, ds_titulo) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                for row in rows:
                    cursor_tgt.execute(insert_sql, tuple(row))
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.chamado OFF")
                tgt_conn.commit()
                logging.info(f"Sincronizados {len(rows)} chamados.")
    except Exception as e:
        logging.error(f"Erro em chamado: {str(e)}")