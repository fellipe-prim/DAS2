import logging
import azure.functions as func

app = func.FunctionApp()

from triggers.extract_analista import bp as extract_analista
from triggers.extract_categoria import bp as extract_categoria 
from triggers.extract_chamado import bp as extract_chamado
from triggers.extract_chamadosla import bp as extract_chamadosla
from triggers.extract_cliente import bp as extract_cliente
from triggers.extract_csat import bp as extract_csat
from triggers.extract_fila import bp as extract_fila
from triggers.extract_sla import bp as extract_sla
from triggers.extract_solicitante import bp as extract_solicitante
from triggers.extract_statushistorico import bp as extract_statushistorico
from triggers.extract_csat_avaliacao import bp as extract_csat_avaliacao

app.register_functions(extract_analista)
app.register_functions(extract_categoria)
app.register_functions(extract_chamado)
app.register_functions(extract_chamadosla)
app.register_functions(extract_cliente)
app.register_functions(extract_csat)
app.register_functions(extract_fila)
app.register_functions(extract_sla)
app.register_functions(extract_solicitante)
app.register_functions(extract_statushistorico)
app.register_functions(extract_csat_avaliacao)
