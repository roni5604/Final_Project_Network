def check_domain(domain):
    domain_split = domain.split(".")
    if len(domain_split) < 2:
        return False
    if domain.startswith("www.") is False:
        return False
    if domain.endswith(".com") is True:
        return True
    if domain.endswith(".co.il") is True:
        return True
    if domain.endswith(".gov.il") is True:
        return True
    if domain.endswith(".net") is True:
        return True
    if domain.endswith(".org") is True:
        return True
    if domain.endswith(".edu") is True:
        return True
    return False
