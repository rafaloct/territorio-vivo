#!/usr/bin/env python3
"""Fail CI if a tracked file could contain real field data or a credential."""
import subprocess
import sys
from pathlib import PurePosixPath
BLOCK_EXT={".m4a",".mp3",".wav",".ogg",".mp4",".mov",".jpg",".jpeg",".heic",".db",".sqlite",".sqlite3",".tvbackup",".zip",".key",".pem",".jks",".keystore"}
BLOCK_PART={"field-data","collected-data","captures","recordings","backups","exports","secrets","private"}
ALLOWED_PREFIX=(".github/","docs/","field-kit/","tools/","tests/","app/","README.md","AGENTS.md",".gitignore","requirements-backup.txt")
def unsafe(path: str) -> bool:
    p=PurePosixPath(path)
    return p.suffix.lower() in BLOCK_EXT or any(part.lower() in BLOCK_PART for part in p.parts) or path.startswith(".env")
def main():
    p=subprocess.run(["git","ls-files","-z"],capture_output=True,check=True)
    files=[f.decode("utf-8","replace") for f in p.stdout.split(b"\x00") if f]
    bad=[f for f in files if unsafe(f)]
    if bad:
        print("BLOQUEADO: arquivos sensiveis rastreados (nomes omitidos). Quantidade:",len(bad))
        sys.exit(1)
    print("Repo guard PASS:",len(files),"arquivos rastreados, nenhum formato de dado bruto proibido.")
if __name__=="__main__":
    main()
