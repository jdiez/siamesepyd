"""To test entry points later on.
"""

from typing import Annotated

import typer

from siamesepyd.core.siamese import MyUuidMetadataBaseModel, SiameseUUID


def main(
    salt: Annotated[str, typer.Option(help="Table format.")] = "ENABL",
    left: Annotated[str, typer.Option(help="Table format.")] = "LUNG342",
    right: Annotated[str, typer.Option(help="Table format.")] = "ABGZMV",
):
    """AI is creating summary for main."""
    Siamese = SiameseUUID(key_seed=salt)  # This could be replaced with project uuid.
    print("Proper UUID (uuid5): ", Siamese(MyUuidMetadataBaseModel(salt=left)))
    print(f"Validated '{left}', '{right}': ", Siamese.validate_keys(left, right))


if __name__ == "__main__":
    typer.run(main)
