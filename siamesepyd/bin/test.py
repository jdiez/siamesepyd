"""To test entry points later on.
"""

import json
from typing import Annotated

import typer
from loguru import logger
from rich import print_json

from siamesepyd.core.siamese import MyUuidMetadataBaseModel, SiameseUUID


def main(
    salt: Annotated[str, typer.Option(help="Salt to be added.")] = "ENABL",
    left: Annotated[str, typer.Option(help="Left side of siamese key.")] = "LUNG342",
    right: Annotated[str, typer.Option(help="Right side of siamese key.")] = "ABGZMV",
) -> None:
    """AI is creating summary for main."""
    Siamese = SiameseUUID(key_seed=salt)  # This could be replaced with project uuid.
    print_json(json.dumps(Siamese(MyUuidMetadataBaseModel(salt=left))._asdict(), indent=4))
    res = Siamese.validate_keys(left, right)
    match res:
        case True:
            logger.success(f"Validation: '{left}' vs '{right}': True")
        case False:
            logger.error(f"Validation: '{left}' vs '{right}': False")
        case _:
            logger.info(f"Validation: '{left}' vs '{right}': {res!r}")


if __name__ == "__main__":
    typer.run(main)
