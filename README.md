# Projeto-MDVRP

Modelo de computação evolucionária baseado no algoritmo genético para o Problema de Roteamento de Veículos com Múltiplos Depósitos, incluindo técnicas de busca local. O algoritmo genético conta com dois operadores de combinação (OBX e PMX) e processos de busca local síncronos e assíncronos com estratégias first improvement, best improvement e ILS modificado.

## IRACE Package 
Procedimento de iterated racing para configuração automática do algoritmo genético. Referência e guia pode ser encontrado em:
(irace: Iterated Racing for Automatic Algorithm Configuration)[https://cran.r-project.org/web/packages/irace/index.html]

### Passos para utilização do pacote

- Instalar R (versão >=3.2.0)
- Instalar irace no console R: install.packages("irace")
- Definir parâmetros - parameters.txt
- Definir lista de instâncias - instances-list.txt
- Configurar cenário - scenario.txt
- Criar diretórios dat e log
- Rodar irace package dentro do diretório irace: Rscript irace-run.R
