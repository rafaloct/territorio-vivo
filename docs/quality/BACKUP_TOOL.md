# Ferramenta independente de backup (para estação confiável)

Esta ferramenta Python CLI usa AES-256-GCM e derivação scrypt para empacotar **pastas de arquivos concluídos e estáveis** em um único `.tvbackup`. Não é o código do aplicativo Flutter nem substitui testes físicos. Use somente em máquina autorizada; não grave senha em argumentos, código, notas nem GitHub. Transfira a cópia para outra mídia e verifique lá.

Instalar dependência em ambiente isolado: `python -m pip install -r requirements-backup.txt`.

Com uma pasta de arquivos já copiados a partir do dispositivo (nunca uma pasta de SQLite em escrita):

```sh
python tools/field_backup.py create /caminho/arquivos /outra-midia/sessao.tvbackup --session TV-20261009-01
python tools/field_backup.py verify /outra-midia/sessao.tvbackup
python tools/field_backup.py restore /outra-midia/sessao.tvbackup /local/novo-sem-arquivos
```

O script solicita frase de acesso interativamente. Recupere-a por meio aprovado; se for perdida, a cópia criptografada se torna inutilizável. Nunca considere arquivo empacotado uma segunda cópia se ele ainda está no mesmo meio físico. A restauração precisa de destino novo. As cópias temporárias na estação também devem ser protegidas por criptografia de disco e eliminadas conforme protocolo institucional.

Use dados SINTÉTICOS até que a equipe aprove privacidade, cadeia de custódia e ensaio completo.
