"""To test entry points later on.
"""

from typing import Annotated

import typer

from siamesepyd.core.siamese import MyUuidMetadataBaseModel, SiameseUUID


def main(
    input_seed: Annotated[str, typer.Option(help="Table format.")] = "ENABL",
    input_salt: Annotated[str, typer.Option(help="Table format.")] = "LUNG342",
    expected_siamese: Annotated[str, typer.Option(help="Table format.")] = "ABGZMV",
):
    """AI is creating summary for main

    Args:
        input_seed (Annotated[str, typer.Option, optional): [description]. Defaults to "Table format.")]="ENABL".
        input_salt (Annotated[str, typer.Option, optional): [description]. Defaults to "Table format.")]="LUNG342".
        expected_siamese (Annotated[str, typer.Option, optional): [description]. Defaults to "Table format.")]="ABGZMV".
    """
    Siamese = SiameseUUID(key_seed=input_seed)  # This could be replaced with project uuid.
    print("Proper UUID (uuid5): ", Siamese(MyUuidMetadataBaseModel(salt=input_salt)))
    print(f"Validated '{input_salt}', '{expected_siamese}': ", Siamese.validate_keys(input_salt, expected_siamese))
    print(f"Validated '{input_salt}', 'ABGZMY': ", Siamese.validate_keys(input_salt, "ABGZMY"))
    print(f"Validated 'LUNG341', '{expected_siamese}': ", Siamese.validate_keys("LUNG341", expected_siamese))


if __name__ == "__main__":
    typer.run(main)
