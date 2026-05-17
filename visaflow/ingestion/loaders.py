from pathlib import Path


SUPPORTED_TEXT_EXTENSIONS = {".txt", ".md"}


def load_document(path: str) -> str:
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix in SUPPORTED_TEXT_EXTENSIONS:
        return file_path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        # Placeholder for richer PDF parsing later.
        raise NotImplementedError(
            "PDF parsing is planned next. For now, provide text exports or .txt samples."
        )

    raise ValueError(f"Unsupported file type: {suffix}")
