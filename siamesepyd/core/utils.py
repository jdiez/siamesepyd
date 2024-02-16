import re
from typing import Callable


def normalizer(
    data: str,
    clean: str = r"[^0-9A-Za-z\s]+",
    polish: str = "(^-+|-+$)",
    rep_str: str = "",
    clean_rep: str = "_",
    uplow: Callable = lambda x: x.lower(),
) -> str:
    r"""AI is creating summary for normalizer

    Args:
        data (str): [description]
        clean (str, optional): [description]. Defaults to "[^0-9A-Za-z\s]+".
        polish (str, optional): [description]. Defaults to "(^-+|-+$)".
        rep_str (str, optional): [description]. Defaults to "".
        clean_rep (str, optional): [description]. Defaults to "_".
        uplow (Callable, optional): [description]. Defaults to lambda x: x.upper().

    Returns:
        str: [description]
    """
    try:
        data = uplow(data.strip())
    except Exception:
        return None  # non string will return None
    else:
        clean_string = re.sub(clean, rep_str, data)
        result = re.sub(r"\s+", clean_rep, clean_string)
    return result
