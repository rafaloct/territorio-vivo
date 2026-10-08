# Três gates independentes antes do uso em campo

Status inicial: **NO-GO**. Nenhum teste em emulador, por si só, libera uso no dia 09/10/2026.

## Gate 1: integridade no aparelho
A captura é considerada concluída apenas se o áudio, foto ou texto foi persistido, reaberto e verificado. Checar ID, bytes e SHA-256. Testar modo avião, app reiniciado, permissões negadas e captura interrompida. Reportar PENDING/FAILED com clareza, jamais sucesso presumido.

## Gate 2: cópia em outro meio físico
Exportar cópia criptografada para outro dispositivo ou mídia USB. Reabrir a cópia e conferir manifesto, quantidade de arquivos, tamanhos e hashes. Preservar originais. Cópia no mesmo armazenamento não conta como redundância.

## Gate 3: recuperação comprovada
Recuperar cópia em destino separado; conferir arquivos e SHA-256 do manifesto; reproduzir áudio e abrir foto de teste, verificando vínculos às sessões. Registrar assinatura/checklist do operador fora do GitHub.

## Testes mínimos com dados sintéticos
- Modo avião e perda de rede, antes e depois da coleta.
- Reinício abrupto durante gravação e após captura confirmada.
- GPS/microfone/câmera negados individualmente.
- Falha de armazenamento e exportação cancelada.
- Arquivo corrompido em cópia fictícia: verificador deve rejeitar.
- Teste independente em aparelho físico e mídia externa.

G1 PASS + G2 PASS + G3 PASS + consentimentos/pactuação + kit impresso = possibilidade de liberação humana. Qualquer falha ou desconhecido = NO-GO. Nunca prometer risco zero.

## Plano B obrigatório
Sem app: usar gravador e câmera nativos, se autorizados, registrar IDs dos arquivos e evidências em papel. Sem energia: mapa falado e árvore de problemas em folhas grandes, fichas de entrevista e diário de campo. Sem internet/transcrição: salvar localmente e transcrever depois.
