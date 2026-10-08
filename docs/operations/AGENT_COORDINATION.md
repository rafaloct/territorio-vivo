# Coordenação ACP: GitHub como fila e memória operacional

Inspirado no trabalho separado do NERUDS Control Center e no padrão GitHub-first, SEM copiar infraestrutura, dados ou credenciais desses projetos.

## Ciclo

Issue delimitada -> executor SWE-2/Devin/Codex -> branch/worktree exclusiva -> draft PR -> testes -> auditoria -> human gate -> integração SOMENTE com autorização específica.

Rótulos de fila: agent:ready, agent:working, agent:review, agent:merge-candidate, human-gate, agent:executor:swe2, safety:blocker, field:gate. Em cada Issue, apenas um estado de lifecycle.

Antes de aceitar:
1. Conferir branches, PRs abertos e sobreposição de caminhos.
2. Uma Issue por sessão. Só aceitar agent:ready com HUMAN_GATE=NO e critérios testáveis.
3. Deixar checkpoint no corpo/comentário da Issue antes de editar.
4. Usar feat/ISSUE-assunto, fix/ISSUE-assunto ou docs/ISSUE-assunto.
5. Abrir PR draft com Issue, base/head SHA, arquivos alterados, testes, impacto em dados, rollback e fallback.
6. Revisar artefatos e sinalizar agent:merge-candidate apenas se tests/gates reais passaram.
7. Nunca dar merge automaticamente. MERGE_ALLOWED=NO até decisão explícita sobre SHA.

## Autoridade humana

Protegido por human-gate: coleta real, qualquer ação em dispositivo com dados, aprovação de consentimento/privacidade, cloud e sincronização, contas e credenciais, assinatura e distribuição APK, substituição do kit físico, operações destrutivas, política de retenção.

Nenhum agente pode marcar FIELD_READY com base somente em testes de unidade ou emulador. Exigir dispositivos reais + modo avião + cópia em segunda mídia + restauração completa + validação da equipe responsável.

## Checkpoint

```
TASK_ID=
OWNER=
BRANCH=
PR=
BASE_SHA=
HEAD_SHA=
OBSERVED=
TARGET=
TESTS=
GATE_1=
GATE_2=
GATE_3=
PHYSICAL_FALLBACK=
HUMAN_GATE=
MERGE_ALLOWED=NO
FIELD_READY=NO
NEXT_ACTION=WAIT_COORDINATOR
```

Os agentes não devem operar recursivamente sobre outras Issues após esse checkpoint.
