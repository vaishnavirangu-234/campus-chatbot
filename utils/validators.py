def validate_query(query: str) -> bool:
    """
    Validates user input query.
    Returns True if valid, else False.
    """

    if not query:
        return False

    if not isinstance(query, str):
        return False

    query = query.strip()

    if len(query) < 2:
        return False

    return True


def validate_event(event: dict) -> bool:
    required_fields = [
        "title",
        "date",
        "time",
        "venue"
    ]

    for field in required_fields:
        if field not in event:
            return False

    return True


def validate_club(club: dict) -> bool:
    required_fields = [
        "name",
        "category",
        "description"
    ]

    for field in required_fields:
        if field not in club:
            return False

    return True


def validate_facility(facility: dict) -> bool:
    required_fields = [
        "name",
        "location",
        "timings"
    ]

    for field in required_fields:
        if field not in facility:
            return False

    return True