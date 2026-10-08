# Arquitetura alvo de coleta offline-first

## Limites

Repositório próprio e banco próprio. Não editar Tutor TDS, NERUDS Control Center nem NERUDS Portal. Nenhuma dependência de cloud para coletar.

## Android/Flutter (a implementar)

UI de sessão e localidade -> domínio (sessões, evidências, problemas, pontos) -> repositórios -> SQLite local + arquivos no sandbox privado. O áudio/foto original NÃO pode ser base64 em logs/Issue. Banco é índice dos arquivos, não substituto da mídia.

Sequência segura da captura: criar ID, registrar intenção PENDING em transação, gravar mídia em nome temporário privado, finalizar fluxo, flush apropriado, medir bytes/hash, renomear para nome definitivo, transacionar VERIFIED. Se interrupção, reconciliar PENDING e temporários na retomada. A transação SQLite não inclui transação do filesystem, então nunca mostrar sucesso antes da confirmação nas duas partes.

Persistência local precisa ser retestada após permissões negadas, quedas, storage cheio e reinícios. Garantir versionamento de esquema e migrações não destrutivas. Aplicativo não limpa originais ao compartilhar/exportar.

## Pacote de exportação

Manifesto v1 com session_id, caminhos relativos sanitizados, tamanhos, SHA-256 e timestamp de criação. Encapsulamento criptografado autenticado. Operador só considera backup concluído após inspeção de cópia externa e restauração testada. A ferramenta Python independente é utilitário de QA e cópia manual em estação confiável, não prova de implementação Flutter.

## Etapas futuras

MVP: formulário local, multimídia, árvore de problemas, comprovantes de salvamento, backup/restore local. Fase 2: mapa offline, sync com opt-in e autorização formal, transcrição assíncrona com revisão. Fase 3: análise e documentação acadêmica, matriz de fontes e visualização de alterações.
