import logging
import os
import azure.functions as func
import pyodbc

bp = func.Blueprint()

@bp.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def extract_sla(myTimer: func.TimerRequest) -> None:
    logging.info('Sincronizando Tabela: itsm.sla')
    
    # Strings de Conexão
    src_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_SOURCE')};DATABASE={os.getenv('SQL_DATABASE_SOURCE')};UID={os.getenv('SQL_USER_SOURCE')};PWD={os.getenv('SQL_PASSWORD_SOURCE')};Encrypt=yes;TrustServerCertificate=no;"
    tgt_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_TARGET')};DATABASE={os.getenv('SQL_DATABASE_TARGET')};UID={os.getenv('SQL_USER_TARGET')};PWD={os.getenv('SQL_PASSWORD_TARGET')};Encrypt=yes;TrustServerCertificate=no;"

    try:
        # EXTRACT: Busca na Origem
        with pyodbc.connect(src_conn_str) as src_conn:
            cursor_src = src_conn.cursor()
            cursor_src.execute("""
                SELECT id_sla, cd_sla, nm_sla, qt_meta_minutos, ds_descricao, fl_ativo, 
                       dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem 
                FROM itsm.sla
            """)
            rows = cursor_src.fetchall()

        if rows:
            # LOAD: Insere no seu banco
            with pyodbc.connect(tgt_conn_str) as tgt_conn:
                cursor_tgt = tgt_conn.cursor()
                
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.sla ON")
                cursor_tgt.execute("DELETE FROM itsm.sla")
                
                insert_sql = """
                    INSERT INTO itsm.sla (id_sla, cd_sla, nm_sla, qt_meta_minutos, ds_descricao, fl_ativo, 
                                         dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                for row in rows:
                    cursor_tgt.execute(insert_sql, tuple(row))
                
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.sla OFF")
                tgt_conn.commit()
                logging.info(f"Sucesso! {len(rows)} SLAs sincronizados.")

    except Exception as e:
        logging.error(f"Erro em sla: {str(e)}")