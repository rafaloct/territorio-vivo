# Contrato obrigatório para agentes: Território Vivo

Leia PRIMEIRO README.md, docs/quality/THREE_GATES.md, docs/security/DATA_POLICY.md, docs/field/2026-10-09_RUNBOOK.md, docs/methodology/DRP.md e docs/operations/AGENT_COORDINATION.md.

## Prioridade absoluta: não perder dados

- Nunca coletar dados reais para testar software. Usar fixtures sintéticas.
- Não apagar, sobrescrever, migrar destrutivamente, limpar cache, reinstalar aplicativo de campo ou reformatar dispositivo/mídia sem autorização explícita do responsável e cópia verificada.
- Banco SQLite e arquivos de mídia são uma unidade lógica: persistir metadados e arquivo por etapas idempotentes, com estado 'pendente/gravando/confirmado'; gravação em arquivo temporário, finalizar, validar, renomear e confirmar banco. Retomar após interrupções. Não prometer atomicidade impossível entre SQLite e FS.
- Não limpar dados locais depois de sync nem depois de exportar.
- Só marcar BACKUP_VERIFIED quando o conteúdo efetivamente for relido e seus hashes baterem; só marcar RESTORE_TESTED após recuperar arquivos para local separado.
- IA/transcrição/operação de rede nunca impedem gravação local. Preservar originais e autoria do relato.
- Capturas com imagens, nomes, voz e coordenadas podem ser dados pessoais/sensíveis; não expor em GitHub, CI, logs nem snapshots. Consentimento granular e controle de acesso obrigatórios.

## Fluxo GitHub-first ACP

- Verifique Issues, PRs e escopos concorrentes. Uma tarefa por passagem do agente e branch/worktree isolada.
- Issue deve ter TASK_ID, objetivo único, caminhos permitidos, fora de escopo, testes, human-gate.
- Registre o estado da tarefa em Issue; abra PR como draft. Não mescle nem faça push forçado sem autorização humana explícita.
- MERGE_ALLOWED=NO; DEPLOY_ALLOWED=NO; RELEASE_FIELD_ALLOWED=NO por padrão.
- CI verde é evidência técnica, não liberação de campo.
- Não acionar serviços pagos, nuvem ou credenciais sem aprovação. Sem desenvolvimento em repositórios vizinhos.
- Após duas tentativas mal-sucedidas do mesmo erro, parar e produzir diagnóstico reproduzível.
- Checkpoint obrigatório: TASK_ID, BRANCH, PR, BASE_SHA, HEAD_SHA, TESTS, GATES, HUMAN_GATE, BLOCKER, NEXT_ACTION.
- Não iniciar automaticamente nova Issue após fechar o checkpoint.

## Regra de segurança de pesquisa

- Respeitar pactuação com a comunidade; não presumir que toponímia ou limites narrados são oficiais.
- Consentimento para gravação/foto/GPS e finalidade; recusa não bloqueia participação na oficina.
- Nunca inferir identidade, propriedade ou localização de pessoas com IA. Falas e sínteses da IA precisam de revisão humana.
- Em caso de conflito entre velocidade e resiliência, escolher o fallback manual e sinalizar claramente NÃO PRONTO.

## Contratos de aceitação

Todas as funcionalidades devem documentar: comportamento offline, recuperação após encerramento forçado, tolerância a permissão negada, impacto de falta de armazenamento, evidência de teste, privacidade, rollback e fallback físico.
