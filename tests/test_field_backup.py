"""Backup tests use generated artificial byte sequences, never real research data."""
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "tools"))
from field_backup import create_pack, verify_pack, restore_pack

class BackupTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.src=self.root/"synthetic"
        (self.src/"nested").mkdir(parents=True)
        (self.src/"nested"/"fake-audio.bin").write_bytes(b"FAKE_AUDIO_BYTES" * 103)
        (self.src/"fake-notes.txt").write_text("Exemplo artificial sem pessoas.\n",encoding="utf-8")
        self.pw="TEST_ONLY_PASSWORD_12345678"
        self.pkg=self.root/"copy.tvbackup"
    def test_backup_restore_verified(self):
        stats=create_pack(self.src,self.pkg,self.pw,"TV-TEST-001")
        self.assertEqual(stats["files"],2)
        self.assertEqual(verify_pack(self.pkg,self.pw)["files"],2)
        out=self.root/"restored"
        self.assertTrue(restore_pack(self.pkg,out,self.pw)["verified"])
        for f in self.src.rglob("*"):
            if f.is_file():
                self.assertEqual(f.read_bytes(),(out/f.relative_to(self.src)).read_bytes())
        with self.assertRaises(FileExistsError):
            restore_pack(self.pkg,out,self.pw)
    def test_wrong_password(self):
        create_pack(self.src,self.pkg,self.pw)
        with self.assertRaises(Exception):
            verify_pack(self.pkg,"TEST_ONLY_WRONG_PASSWORD_123")
    def test_tamper_detected(self):
        create_pack(self.src,self.pkg,self.pw)
        with self.pkg.open("r+b") as p:
            p.seek(60)
            old=p.read(1)
            p.seek(60)
            p.write(bytes([old[0]^4]))
        with self.assertRaises(Exception):
            verify_pack(self.pkg,self.pw)
    def test_no_overwrite(self):
        create_pack(self.src,self.pkg,self.pw)
        with self.assertRaises(FileExistsError):
            create_pack(self.src,self.pkg,self.pw)
    def test_no_inside_source(self):
        with self.assertRaises(ValueError):
            create_pack(self.src,self.src/"bad.tvbackup",self.pw)
    def test_empty_source_rejected(self):
        empty=self.root/"empty";empty.mkdir()
        with self.assertRaises(ValueError):
            create_pack(empty,self.pkg,self.pw)
if __name__=="__main__":
    unittest.main()
