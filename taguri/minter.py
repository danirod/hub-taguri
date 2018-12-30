import unittest
from taguri.validator import (
    authority_name_validator,
    date_validator,
    specific_validator,
)

class TagUriMinter:
    """Minter to build tag URIs.

    The minter is able to form valid tag URIs in conformance with RFC
    4151, given the components that belong to the tag URI; namely, the
    authority name and the date of the tagging entity, the specific
    part of the tag, and optionally a fragment.

    Note:
        Authority names can either be e-mail addresses or DNS names.
        The validator is not too strict when accepting or rejecting
        authority names, which means that invalid e-mail addresses and
        unqualified domain names will be accepted by the validator.
        This is intentional by design.

        Note that, because DNS names and e-mail addresses are supposed
        to map to valid domain names or e-mail addresses owned by the
        entity on behalf of the tags, it's not recommended to use
        invalid e-mail addresses anyway, as it's highly probable that
        an invalid e-mail address will be rejected by most mail systems
        out there.

    Args:
        authority_name (str): Authority name on behalf of who the tags
            will be minted.  See the aditional note on authority names
            to see appropiate authority names.
        date (str): Date to set the tagging entity part of the tag to.
            It has to be a date compliant with RFC 3339 (or ISO 8601).
    
    Raises:
        AttributeError: if the given authority name or date cannot be
            properly validated.  To be valid, an authority name has to
            either be a DNS name or an e-mail address, and the date must
            follow the formatting rules described in the notes and in
            the RFC.
    """

    def __init__(self, authority_name: str, date: str):
        if not authority_name_validator(authority_name):
            # The authority name is not valid.
            raise AttributeError(f'Invalid authority name: {authority_name}')
        else:
            self.__authority_name = authority_name
        
        if not date_validator(date):
            # The date is not valid.
            raise AttributeError(f'Invalid date: {date}')
        else:
            self.__date = date
    
    @property
    def authority_name(self) -> str:
        """str: The authority name on behalf of the generated tags.
        
        The value returned by this property equals to the given
        `authority_name` argument when instantiating the minter.
        """
        return self.__authority_name
    
    @property
    def date(self) -> str:
        """str: The date used for the current tagging entity.
        
        The value returned by this property equals to the given
        `date` argument when instantiating the minter.
        """
        return self.__date

    @property
    def tagging_entity(self) -> str:
        """str: The entire tagging entity for this minter.

        The tagging entity is built using the given authority name and
        date at instantiation time of the class instance, separated by
        a comma.

        Example:
            >>> minter = TagUriMinter('alice.example.com', '2018-11-26')
            >>> minter.tagging_entity
            'alice.example.com,2018-11-26'
        """
        return f"{self.authority_name},{self.date}"

    @property
    def prefix(self) -> str:
        """str: The tagging entity for the minter, prefix included.

        This property will return the tagging entity that is built using
        the given authority name and date, like ``tagging_entity``.
        However, this property will also include the `tag:` prefix.

        Example:
            >>> minter = TagUriMinter('alice.example.com', '2018-11-26')
            >>> minter.prefix
            'tag:alice.example.com,2018-11-26'
        """
        return f"tag:{self.authority_name},{self.date}"
    
    def mint(self, specific: str, fragment: str=None) -> str:
        """
        Mints a new tag URI using the given specific and fragment.

        This method will return the string representation of the tag
        built using the given tagging entity when the minter was
        instantiated, plus the given specific as an argument.  If a
        fragment is given, it's also added at the end of the built tag.

        Args:
            specific (str): the specific part of the tag to use.
            fragment (obj:`str`, optional): if given, the fragment part
                of the tag. Will be appended to the specific part of
                the tag using a `#` symbol.
        
        Returns:
            str: the built tag using the given input properties.
        
        Raises:
            AttributeError: if the given specific or fragment part of
                the tag don't pass the validation test for a valid
                specific or fragment part.
        
        Examples:
            >>> minter = TagUriMinter('alice.example.com', '2018-11')
            >>> minter.mint('Collections/Books')
            'tag:alice.example.com,2018-11:Collections/Books'

            >>> minter.mint('Collections/Books', 'Doe')
            'tag:alice.example.com,2018-11:Collections/Books#Doe'
        """
        if not specific_validator(specific):
            raise AttributeError(f'Invalid specific: {specific}')
        if fragment:
            if not specific_validator(fragment):
                raise AttributeError(f'Invalid fragment: {fragment}')
            return f'{self.prefix}:{specific}#{fragment}'
        else:
            return f'{self.prefix}:{specific}'