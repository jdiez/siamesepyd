"""To test entry points later on.
"""

from siamesepyd.core.shortids import MyUuidMetadataBaseModel, SiameseUUID


def main():
    Siamese = SiameseUUID(key_seed="ENABL")  # This could be replaced with project uuid.
    print("Proper UUID (uuid5): ", Siamese(MyUuidMetadataBaseModel(salt="LUNG342")))
    print("Validated 'LUNG342', 'ABGZMV': ", Siamese.validate_keys("LUNG342", "ABGZMV"))
    print("Validated 'LUNG342', 'ABGZMY': ", Siamese.validate_keys("LUNG342", "ABGZMY"))
    print("Validated 'LUNG341', 'ABGZMV': ", Siamese.validate_keys("LUNG341", "ABGZMV"))


if __name__ == "__main__":
    main()
