#!/usr/bin/env python3
"""Encrypted, integrity-checked portable field backup (synthetic tests only).
Never pass real passwords on a command line or place field data in this repo.
"""
from __future__ import annotations
import argparse
import getpass
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
from datetime import datetime, timezone
import uuid
import zipfile

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

MAGIC = b"TVPKG01\x00"
SALT_LEN = 16
NONCE_LEN = 12
TAG_LEN = 16
BUF = 1024 * 1024
MAX_FILES = 100000
MAX_BYTES = 40 * 1024**3

def _key(passphrase: str, salt: bytes) -> bytes:
    if not isinstance(passphrase, str) or len(passphrase) < 12:
        raise ValueError("Senha insuficiente; use frase longa de pelo menos 12 caracteres.")
    return hashlib.scrypt(passphrase.encode("utf-8"), salt=salt,
                          n=2**14, r=8, p=1, dklen=32, maxmem=64*1024*1024)

def _valid_relative(value: str) -> bool:
    p = PurePosixPath(value)
    return bool(value and not value.startswith(("/", "\\")) and "\\" not in value
                and ":" not in value and p.as_posix() == value
                and all(x not in (".", "..", "") for x in p.parts))

def _inventory(source: Path):
    if not source.is_dir() or source.is_symlink():
        raise ValueError("Origem deve ser pasta real.")
    records = []
    total = 0
    for p in sorted(source.rglob("*")):
        if p.is_symlink():
            raise ValueError("Links simbolicos nao permitidos.")
        if p.is_dir():
            continue
        if not p.is_file():
            raise ValueError("Arquivo especial nao permitido.")
        rel = p.relative_to(source).as_posix()
        if not _valid_relative(rel):
            raise ValueError("Caminho nao seguro.")
        h = hashlib.sha256()
        size = 0
        with p.open("rb") as f:
            for chunk in iter(lambda:f.read(BUF), b""):
                h.update(chunk); size += len(chunk)
        records.append({"path": rel, "size": size, "sha256": h.hexdigest()})
        total += size
        if len(records) > MAX_FILES or total > MAX_BYTES:
            raise ValueError("Pasta excede limites de seguranca.")
    if not records:
        raise ValueError("Origem sem arquivos; nao ha o que salvar.")
    return records

class _EncryptedSink:
    def __init__(self, stream, encryptor):
        self.stream, self.encryptor, self.pos = stream, encryptor, 0
    def write(self, data):
        self.stream.write(self.encryptor.update(data))
        self.pos += len(data)
        return len(data)
    def tell(self):
        return self.pos
    def flush(self):
        self.stream.flush()

def create_pack(source, target, passphrase, session_id=None):
    source, target = Path(source).resolve(), Path(target).resolve()
    if source == target or source in target.parents:
        raise ValueError("Backup deve ficar fora da pasta de origem.")
    if target.exists():
        raise FileExistsError("O arquivo destino ja existe; nao sobrescrever.")
    target.parent.mkdir(parents=True, exist_ok=True)
    items = _inventory(source)
    meta = {"schema":"territorio-vivo-backup-v1",
            "package_id":str(uuid.uuid4()),
            "session_id":session_id or "UNSPECIFIED",
            "created_utc":datetime.now(timezone.utc).isoformat(),
            "files":items}
    salt, nonce = os.urandom(SALT_LEN), os.urandom(NONCE_LEN)
    header = MAGIC + salt + nonce
    key = _key(passphrase, salt)
    tmp = target.with_name(target.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with tmp.open("xb") as f:
            f.write(header)
            encryptor = Cipher(algorithms.AES(key), modes.GCM(nonce)).encryptor()
            encryptor.authenticate_additional_data(header)
            sink = _EncryptedSink(f, encryptor)
            with zipfile.ZipFile(sink, "w", compression=zipfile.ZIP_DEFLATED,
                                 compresslevel=6, allowZip64=True) as z:
                z.writestr("manifest.json", json.dumps(meta, ensure_ascii=False, sort_keys=True))
                for item in items:
                    p = source / item["path"]
                    h, n = hashlib.sha256(), 0
                    with p.open("rb") as inp, z.open("data/" + item["path"], "w") as out:
                        for chunk in iter(lambda:inp.read(BUF), b""):
                            out.write(chunk); h.update(chunk); n += len(chunk)
                    if n != item["size"] or h.hexdigest() != item["sha256"]:
                        raise RuntimeError("Origem mudou durante backup; repetir.")
            f.write(encryptor.finalize())
            f.write(encryptor.tag)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()
    return {"files":len(items), "bytes":sum(x["size"] for x in items),
            "package_bytes":target.stat().st_size, "package_id":meta["package_id"]}

def _decrypted_temp(package, passphrase):
    package = Path(package)
    length = package.stat().st_size
    header_len = len(MAGIC) + SALT_LEN + NONCE_LEN
    if length <= header_len + TAG_LEN:
        raise ValueError("Pacote muito curto.")
    plain = tempfile.TemporaryFile(mode="w+b")
    try:
        with package.open("rb") as f:
            header = f.read(header_len)
            if not header.startswith(MAGIC):
                raise ValueError("Formato de pacote nao reconhecido.")
            salt = header[len(MAGIC):len(MAGIC)+SALT_LEN]
            nonce = header[-NONCE_LEN:]
            f.seek(-TAG_LEN, os.SEEK_END)
            tag = f.read(TAG_LEN)
            f.seek(header_len)
            decryptor = Cipher(algorithms.AES(_key(passphrase,salt)), modes.GCM(nonce, tag)).decryptor()
            decryptor.authenticate_additional_data(header)
            remaining = length - header_len - TAG_LEN
            while remaining:
                block = f.read(min(BUF, remaining))
                if not block:
                    raise ValueError("Pacote incompleto.")
                plain.write(decryptor.update(block))
                remaining -= len(block)
            plain.write(decryptor.finalize())
        plain.seek(0)
        return plain
    except Exception:
        plain.close()
        raise

def _validated_zip(plain):
    z = zipfile.ZipFile(plain, "r")
    paths = z.namelist()
    if not paths or paths.count("manifest.json") != 1 or len(paths) > MAX_FILES + 1:
        raise ValueError("Estrutura incompleta ou suspeita.")
    if len(paths) != len(set(paths)):
        raise ValueError("Entradas duplicadas.")
    with z.open("manifest.json") as f:
        meta = json.load(f)
    if meta.get("schema") != "territorio-vivo-backup-v1":
        raise ValueError("Versao de manifesto nao suportada.")
    records = meta.get("files")
    if not isinstance(records, list) or not records or len(records) > MAX_FILES:
        raise ValueError("Manifesto invalido.")
    allowed = {"manifest.json"}
    total = 0
    for item in records:
        rel, size, expected = item["path"], item["size"], item["sha256"]
        if not _valid_relative(rel) or not isinstance(size,int) or size<0 or len(expected)!=64:
            raise ValueError("Entrada insegura ou invalida.")
        allowed.add("data/"+rel)
        total += size
        if total > MAX_BYTES:
            raise ValueError("Conteudo excede limite.")
    if set(paths) != allowed:
        raise ValueError("Arquivos divergentes do manifesto.")
    for item in records:
        h, n = hashlib.sha256(), 0
        with z.open("data/"+item["path"],"r") as f:
            for chunk in iter(lambda:f.read(BUF),b""):
                h.update(chunk); n += len(chunk)
                if n > item["size"]:
                    raise ValueError("Tamanho excede manifesto.")
        if n != item["size"] or h.hexdigest() != item["sha256"]:
            raise ValueError("Hash ou tamanho divergente.")
    return z, meta

def verify_pack(package, passphrase):
    with _decrypted_temp(package,passphrase) as plain:
        z, m = _validated_zip(plain)
        with z:
            return {"files":len(m["files"]),"bytes":sum(i["size"] for i in m["files"]),
                    "package_id":m["package_id"],"verified":True}

def restore_pack(package, destination, passphrase):
    dest = Path(destination).resolve()
    if dest.exists():
        raise FileExistsError("Restaurar apenas em destino novo, sem sobrescrever.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with _decrypted_temp(package, passphrase) as plain:
        z, m = _validated_zip(plain)
        tmpdir = Path(tempfile.mkdtemp(prefix=".tv-restore-", dir=str(dest.parent)))
        try:
            with z:
                for item in m["files"]:
                    p = tmpdir / item["path"]
                    p.parent.mkdir(parents=True,exist_ok=True)
                    with z.open("data/"+item["path"]) as inp, p.open("xb") as out:
                        shutil.copyfileobj(inp, out, BUF)
            if _inventory(tmpdir) != m["files"]:
                raise ValueError("Restauracao diverge do manifesto.")
            os.replace(tmpdir,dest)
        finally:
            if tmpdir.exists():
                shutil.rmtree(tmpdir)
    return {"verified":True,"files":len(m["files"]),"restored_dir":str(dest)}

def main():
    p = argparse.ArgumentParser(description="Backup de campo autenticado AES-GCM; nunca usar senha na linha de comando.")
    sub = p.add_subparsers(dest="action", required=True)
    create = sub.add_parser("create"); create.add_argument("source"); create.add_argument("output")
    create.add_argument("--session",default="UNSPECIFIED")
    verify = sub.add_parser("verify"); verify.add_argument("package")
    restore = sub.add_parser("restore"); restore.add_argument("package"); restore.add_argument("destination")
    args = p.parse_args()
    pw = getpass.getpass("Senha de cifragem (não aparece): ")
    if args.action == "create":
        confirm = getpass.getpass("Confirmar senha: ")
        if pw != confirm:
            p.error("Senhas nao conferem.")
        result = create_pack(args.source,args.output,pw,args.session)
    elif args.action == "verify":
        result = verify_pack(args.package,pw)
    else:
        result = restore_pack(args.package,args.destination,pw)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
