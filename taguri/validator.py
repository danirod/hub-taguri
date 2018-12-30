import re
from datetime import datetime

EMAIL_USER_RE = re.compile(r"^([0-9a-zA-Z\.\-\_\+]+)$")
DNSCOMP_RE = re.compile(r"^([a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?)$")
PCT_HEX_TOKEN_RE = re.compile(r"^([0-9a-fA-F]{2})")

def authority_name_validator(authority_name: str) -> bool:
    """Tests whether the given authority_name is valid per the RFC.

    To be valid, an authority_name has to be either an e-mail address
    or a DNS name.  However, the RFC also admits that the parsers should
    be future-proof in case the spec is ever updated to allow additional
    namespaces to be used as an authority_name, such as a telephone
    number assigned to an entity at a given point in time.  Therefore,
    the RFC suggests that validators and parsers should not be strict
    enough to reject authority names that are not semantically valid.

    As an example, this validator will successfully validate a DNS name
    that is not a FQDN (such as an unqualified domain name with no dots,
    such as the ones found in local Microsoft Windows networks).  The
    validator will also successfully validate e-mail addresses that do
    not conform to the e-mail RFC, such as `.john.doe.@example.com`.

    Args:
        authority_name (str): the given authority name to validate.
    
    Returns:
        bool: True if the given authority name is valid; else False.
    
    Examples:
        >>> authority_name_validator('example.org')
        True

        >>> authority_name_validator('johndoe@example.org')
        True

        >>> authority_name_validator('Windows-PC')
        True

        >>> authority_name_validator('.john.doe.@example.com')
        True

        >>> authority_name_validator('no,commas,here,please')
        False
    """

    def validate_dns_name(dns_name: str) -> bool:
        # DNSname = DNScomp *( "."  DNScomp ) ; see RFC 1035 [3]
        # DNScomp = alphaNum [*(alphaNum /"-") alphaNum]
        # alphaNum = DIGIT / ALPHA
        if dns_name.startswith('.') or dns_name.endswith('.'):
            return False
        else:
            for dns_comp in dns_name.split('.'):
                if not DNSCOMP_RE.match(dns_comp):
                    return False
            return True
    
    def validate_email_address(email_address: str) -> bool:
        # emailAddress = 1*(alphaNum /"-"/"."/"_") "@" DNSname
        # There exists an errata in the RFC that warns that this regex
        # will reject e-mail addresses having the + symbol. This
        # function takes that into account.
        if len(email_address.split('@')) != 2:
            return False
        else:
            username, dns_name = email_address.split('@')
            return EMAIL_USER_RE.match(username) and validate_dns_name(dns_name)
    
    if len(authority_name.split('@')) == 2:
        return validate_email_address(authority_name)
    else:
        return validate_dns_name(authority_name)

def date_validator(date: str) -> str:
    """Tests whether the given date is valid according to the RFC.

    Valid dates are instances of the RFC 3339, which is at the same
    time a profile of ISO 8601.  Valid dates must provide the year,
    optionally the month; and if the month is provided, then optionally
    a day.

    Examples of valid dates are 2018, 2018-11 and 2018-11-22.

    Args:
        date (str): the given date to validate.
    
    Returns:
        bool: True if the date is valid, otherwise False.
    
    Examples:
        >>> date_validator('2017')
        True

        >>> date_validator('2018-04')
        True

        >>> date_validator('2018-12-31')
        True

        >>> date_validator('2018-11-29T14:04:02-05:00')
        False

        >>> date_validator('year')
        False

        >>> date_validator('341-11-22')
        False

        >>> date_validator('0341-11-22')
        True

        >>> date_validator('1999-12-32')
        False
    """
    for format in ('%Y-%m-%d', '%Y-%m', '%Y'):
        try:
            datetime.strptime(date, format)
        except ValueError:
            pass
        else:
            return True
    return False

def specific_validator(specific: str) -> str:
    """Validates the specifics or fragment tokens of a tag.

    The specific has to be a string of characters specifically allowed
    by the grammar.  A string can be empty.  The grammar for tag URI
    considers valid tokens <pchar>, `/` and `?`, being pchar defined
    in RFC 3986.

    Args:
        specific (str): a specific string to validate.
    
    Returns:
        bool: True if the string is valid, otherwise False.
    
    Examples:
        >>> specific_validator('path/to/resource.html')
        True

        >>> specific_validator('Customers.JohnDoe')
        True

        >>> specific_validator('<invalid_characters>')
        False

        >>> specific_validator('a space')
        False
    """
    pchar_tokens = (
        '/', '?', # as per specific in RFC 4151
        ':', '@', # as per pchar in RFC 3986
        '-', '.', '_', '~', # as per unreserved in RFC 3986
        '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', '=', # sub-delims
    )

    # Test for pct-encoded, although discouraged by spec.
    pct_encoded_tokens = specific.split('%')
    remainder = [pct_encoded_tokens[0]]
    for pct_encoded_token in pct_encoded_tokens[1:]:
        # Test that they are hexchars.
        if not PCT_HEX_TOKEN_RE.match(pct_encoded_token):
            return False
        remainder.append(pct_encoded_token[2:])
    specific_without_pct_tokens = ''.join(remainder)
    
    # Test for pchar tokens.
    for pchar in list(specific_without_pct_tokens):
        if any((pchar.isdigit(), pchar.isalpha(), pchar in pchar_tokens)):
            continue
        return False
    
    # Valid.
    return True
