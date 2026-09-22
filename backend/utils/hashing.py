import hashlib


def sha256_file(file_path: str) -> str:
    digest = hashlib.sha256()
    with open(file_path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(65536), b''):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()
