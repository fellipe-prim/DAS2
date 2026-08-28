import logging
import os
import azure.functions as func
import pyodbc

bp = func.Blueprint()

@bp.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def extract_categoria(myTimer: func.TimerRequest) -> None:
    logging.info('Sincronizando Tabela: itsm.categoria')
    
    # Strings de Conexão
    src_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_SOURCE')};DATABASE={os.getenv('SQL_DATABASE_SOURCE')};UID={os.getenv('SQL_USER_SOURCE')};PWD={os.getenv('SQL_PASSWORD_SOURCE')};Encrypt=yes;TrustServerCertificate=no;"
    tgt_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv('SQL_SERVER_TARGET')};DATABASE={os.getenv('SQL_DATABASE_TARGET')};UID={os.getenv('SQL_USER_TARGET')};PWD={os.getenv('SQL_PASSWORD_TARGET')};Encrypt=yes;TrustServerCertificate=no;"

    try:
        # EXTRACT: Busca na Origem (Professor)
        with pyodbc.connect(src_conn_str) as src_conn:
            cursor_src = src_conn.cursor()
            cursor_src.execute("""
                SELECT id_categoria, cd_categoria, nm_categoria, ds_descricao, fl_ativo, 
                       dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem 
                FROM itsm.categoria
            """)
            rows = cursor_src.fetchall()

        if rows:
            # LOAD: Insere no seu banco (Target)
            with pyodbc.connect(tgt_conn_str) as tgt_conn:
                cursor_tgt = tgt_conn.cursor()
                
                # Desbloqueia inserção de ID manual
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.categoria ON")
                
                # Limpa a tabela para evitar duplicidade (estratégia simples de EL)
                cursor_tgt.execute("DELETE FROM itsm.categoria")
                
                insert_sql = """
                    INSERT INTO itsm.categoria (id_categoria, cd_categoria, nm_categoria, ds_descricao, fl_ativo, 
                                               dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                for row in rows:
                    cursor_tgt.execute(insert_sql, tuple(row))
                
                cursor_tgt.execute("SET IDENTITY_INSERT itsm.categoria OFF")
                tgt_conn.commit()
                logging.info(f"Sucesso! {len(rows)} categorias sincronizadas.")

    except Exception as e:
        logging.error(f"Erro em categoria: {str(e)}")