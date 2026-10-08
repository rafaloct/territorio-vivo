# Política mínima de segurança de dados de pesquisa

**Dados do campo não são código-fonte.** GitHub private NÃO é repositório de dados pessoais, imagens, vozes, localizações precisas, nomes de entrevistados, banco SQLite, transcrições ou backups.

- Identificadores pseudônimos de sessão, localidade e observação (UUIDs); tabela de ligação com nomes, quando necessária e autorizada, fica separada e protegida.
- Registro de consentimento granular: áudio, foto, coordenada, uso em análise, publicação ou compartilhamento. Cada tipo de permissão é independente. Consentimento pode ser recusado; anotações agregadas e não identificáveis ainda podem ser consideradas conforme protocolo aprovado.
- Orientações de ética e privacidade institucional, LGPD e, quando aplicável, avaliação por CEP/Conep e autorização comunitária devem ser pactuadas antes da coleta. Software não substitui essas decisões.
- Coordenadas de moradias, lugares culturalmente sensíveis e limites contestados não devem ser divulgadas por padrão. Não derivar posse fundiária de mapa falado.
- Manter arquivos originais imutáveis; edições/transcrições ligadas ao original, revisadas, com proveniência e datas. Nunca reescrever o original com resumo por IA.
- Criptografia em repouso no aparelho e em qualquer cópia externa; credenciais em gerenciador seguro, nunca no repo. Armazenamento privado da aplicação, não galeria pública, por padrão.
- Exports apenas com confirmação humana, destino identificado e verificação de integridade. Sem sincronizar automaticamente para nuvem ou IA.
- A equipe deve definir finalidade, responsáveis, período de retenção e eliminação segura. Nenhuma política de prazo é presumida no código.
- Logs: só status e IDs sintéticos; jamais falas, nomes, nomes reais de arquivos, áudio, transcrições ou tokens.
- Testes e CI: fixtures artificiais sem qualquer vínculo real.
- Se suspeita de exposição ou perda: interromper coletas, preservar evidências técnicas sanitizadas, avisar o responsável de pesquisa e seguir o protocolo institucional.
