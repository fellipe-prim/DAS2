import logging
import os
import azure.functions as func
import pyodbc

bp = func.Blueprint()

@bp.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def extract_csat(myTimer: func.TimerRequest) -> None:
    logging.info('Sincronizando: csat')
    
    src_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_SOURCE')};DATABASE={os.getenv('SQL_DATABASE_SOURCE')};UID={os.getenv('SQL_USER_SOURCE')};PWD={os.getenv('SQL_PASSWORD_SOURCE')};Encrypt=yes;TrustServerCertificate=no;"
    tgt_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_TARGET')};DATABASE={os.getenv('SQL_DATABASE_TARGET')};UID={os.getenv('SQL_USER_TARGET')};PWD={os.getenv('SQL_PASSWORD_TARGET')};Encrypt=yes;TrustServerCertificate=no;"

    try:
        # 1. EXTRAIR
        with pyodbc.connect(src_conn_str) as src_conn:
            cursor_src = src_conn.cursor()
            cursor_src.execute("SELECT Id, Column1, Column2 FROM itsm.csat")
            rows = cursor_src.fetchall() # CORREÇÃO AQUI: usando o cursor_src que executou a query

        if rows:
            # 2. CARREGAR
            with pyodbc.connect(tgt_conn_str) as tgt_conn:
                cursor_tgt = tgt_conn.cursor()
                # Tabela CSAT não tem IDENTITY no DDL do professor, então é só deletar e inserir
                cursor_tgt.execute("DELETE FROM itsm.csat")
                
                insert_sql = "INSERT INTO itsm.csat (Id, Column1, Column2) VALUES (?, ?, ?)"
                for row in rows:
                    cursor_tgt.execute(insert_sql, tuple(row))
                
                tgt_conn.commit()
                logging.info(f"Sucesso! {len(rows)} registros na tabela CSAT.")
        else:
            logging.info("Nenhum dado encontrado na tabela CSAT da origem.")

    except Exception as e:
        logging.error(f"Erro em CSAT: {str(e)}")