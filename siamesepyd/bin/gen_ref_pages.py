"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files
from loguru import logger

nav = mkdocs_gen_files.Nav()

src = Path(__file__).parent.parent
logger.debug(f"src: {src}")
dsrc = Path(__file__).parent.parent.parent
logger.debug(f"dsrc: {dsrc}")

for path in sorted(src.rglob("*.py")):
    logger.debug(path)
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(dsrc).with_suffix(".md")
    full_doc_path = Path(dsrc, "docs", doc_path)
    logger.debug(full_doc_path)

    parts = ["siamesepyd", *list(module_path.parts)]
    logger.debug(parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    logger.debug(full_doc_path)
    logger.debug(doc_path)
    logger.debug(doc_path.as_posix())
    logger.debug(parts)

    nav[str(doc_path)] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")
    logger.debug("Full doc path: " + str(full_doc_path))
    logger.debug("path: " + str(path))
    mkdocs_gen_files.set_edit_path(full_doc_path, path)

logger.debug(dsrc / "docs/SUMMARY.md")
with mkdocs_gen_files.open(dsrc / "docs/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
