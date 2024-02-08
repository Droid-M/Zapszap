Tabela de códigos usados na comunicação socket entre computadores

<table><tbody><tr><td><strong>Código</strong></td><td><strong>Significado</strong></td><td><strong>&nbsp; Tratamento</strong></td></tr><tr><td><i>0X01</i></td><td>Solicitação de lista de grupos</td><td>O servidor deve consultar suas listas de grupos (contendo os IPs associados a cada lista) e enviar para o cliente.</td></tr><tr><td>0X02</td><td>Solicita a partição em um grupo</td><td>O servidor deve receber o endereço IP contido na mensagem e armazená-lo em sua lista de ips referentes ao grupo no qual ele está participando</td></tr><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></tbody></table>

Estrutura básica do JSON de pedido (enviado pelo cliente):

*   **code:** informa o tipo de ação da solicitação atual.

Estrutura básica do JSON de resposta (enviado pelo servidor):

*   **success:** booleano que indica se a solicitação do cliente pôde ser atendida com sucesso.
*   **data:** conteúdo da resposta. A estrutura e conteúdo deste campo pode variar de acordo com o tipo de solicitação.