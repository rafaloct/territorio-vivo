# Território Vivo

**Situação em 08/10/2026: NÃO LIBERADO PARA COLETA REAL.** Este repositório contém a governança e as ferramentas de segurança iniciais. A aprovação de uso exige testes no dispositivo e restauração verificada. Documentação não equivale a aplicativo funcional.

Projeto independente para cartografia social, memória territorial, mapa falado e árvore de problemas no DRP, com coleta de fotos, áudios, notas e GPS. Referências citadas na atividade de 09/10: Fazenda Nova, Galião e Itapiru (**grafia, localização e identidade territorial ainda devem ser confirmadas com os participantes**).

## Regra prioritária

A pesquisa continua com papel e instrumentos físicos mesmo sem app. Nunca encerrar o campo somente porque um ícone diz "salvo". O aplicativo é auxiliar, não fonte exclusiva.

## Critério de campo: 3 camadas + contingência

1. **Integridade local:** cada arquivo foi gravado, reaberto e passou na conferência de tamanho e SHA-256.
2. **Cópia independente:** backup criptografado em mídia/dispositivo distinto com manifesto verificável; cópia não apaga a fonte.
3. **Restauração:** pacote de teste foi restaurado em ambiente separado; contagens e hashes batem; responsável assinou o checklist.

**Fallback manual:** gravador nativo quando app falha; câmera nativa se fotos falham; fichas impressas, desenho coletivo e diário físico se tudo falhar. Cada observação recebe o mesmo código de sessão para posterior digitalização.

Consulte [gates](docs/quality/THREE_GATES.md), [manual de campo de 09/10](docs/field/2026-10-09_RUNBOOK.md), [kit imprimível](field-kit/PAPER_KIT.md), [AGENTS](AGENTS.md), [coordenação](docs/operations/AGENT_COORDINATION.md), [metodologia](docs/methodology/DRP.md), [política de dados](docs/security/DATA_POLICY.md).

## Arquitetura alvo

Flutter Android offline-first; base SQLite local e mídias no armazenamento privado; captura atômica, recibos, exportação criptografada, inspeção de integridade; sincronização posterior opt-in, opcional. IA/transcrição nunca bloqueiam gravação e não substituem a fala original. Nenhuma integração com Tutor TDS ou NERUDS Control Center sem decisão e contrato próprios.

## Desenvolvimento

GitHub é a fila e a memória; uma Issue delimitada = branch isolada = PR draft; revisão de segurança antes de mesclar; sem auto-merge. Separar claramente OBSERVED (verificado), TARGET (alvo), BLOCKED (não validado). **Nenhum dado real em commits, Issues, PRs, Actions ou logs.**

## Estado

- [x] Repositório privado separado e governança inicial.
- [ ] App implementado e testado em Android real, com modo avião.
- [ ] Backup criptografado e restauração validados com arquivos sintéticos.
- [ ] Teste físico de exportação para mídia/dispositivo diferente.
- [ ] Autorização metodológica/privacidade, consentimentos e responsável de campo.

**Política:** se qualquer gate falhar, registrar em papel e áudio/câmera nativos autorizados; aplicativo não deve ser apresentado como pronto.
