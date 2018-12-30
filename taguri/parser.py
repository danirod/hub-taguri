from typing import Tuple
from .validator import (
    authority_name_validator,
    date_validator,
    specific_validator,
)

class TagUriParser:
    """Parser used to parse tag URIs.

    The parser is able to extract information from valid tag URIs that
    were crafted in conformance to the RFC 4151, taking out the
    authority name, date, specific, and fragment part of the URI,
    and putting them in properties that can be accessed by Python code.

    Args:
        tag_uri (str): the tag URI to parse.
    
    Raises:
        AttributeError: if the given tag URI is not valid.  The message
        of the raised error will have more information about which part
        of the tag was invalid.
    """

    def __init__(self, tag_uri: str):
        tokens = tag_uri.split(':', maxsplit=2)
        if len(tokens) != 3:
            raise AttributeError('Invalid tag_uri: misses parts')
        else:
            self.__tag = tag_uri
        
        prefix, tagging_entity, specific = tokens

        if prefix != 'tag':
            # This is not a tag unless the prefix is given.
            raise AttributeError('Invalid tag_uri: invalid prefix')
        
        try:
            # We can do this because commas are not allowed here.
            authority_name, date = tagging_entity.split(',')

            # Validates authority name.
            if not authority_name_validator(authority_name):
                raise AttributeError('Invalid tag_uri: invalid authority name')
            self.__authority = authority_name

            # Validates date.
            if not date_validator(date):
                raise AttributeError('Invalid tag_uri: invalid date')
            self.__date = date
        except ValueError:
            # Raised by Python if tagging_entity.split cannot be destructured.
            raise AttributeError('Invalid tag_uri: invalid tagging entity')
        
        # Extract and validate the fragment.
        if '#' in specific:
            try:
                specific, fragment = specific.split('#')
                if not specific_validator(fragment):
                    raise AttributeError('Invalid tag_uri: invalid fragment')
                self.__fragment = fragment
            except ValueError:
                # Raised if specific.split cannot be destructured.
                raise AttributeError('Invalid tag_uri: too many fragments')
        else:
            self.__fragment = None
        
        # Validate specific.
        if not specific_validator(specific):
            raise AttributeError('Invalid tag_uri: invalid specific')
        self.__specific = specific
    
    @property
    def tag(self) -> str:
        """str: The complete tag as parsed by the instantiator.

        This is an identity function that returns the given tag URI
        at the time of instantiating the class, as long as the tag
        URI is valid.

        Example:
            >>> parser = TagUriParser('tag:alice.example.com,2018:Hi')
            >>> parser.tag
            'tag:alice.example.com,2018:Hi'
        """
        return self.__tag
    
    @property
    def authority_name(self) -> str:
        """str: The authority name of the tag.

        Example:
            >>> parser = TagUriParser('tag:alice.example.com,2018:Hi')
            >>> parser.authority_name
            'alice.example.com'
        """
        return self.__authority
    
    @property
    def date(self) -> str:
        """str: The date component of the tag.

        Example:
            >>> parser = TagUriParser('tag:alice.example.com,2018:Hi')
            >>> parser.date
            '2018'
        """
        return self.__date
    
    @property
    def tagging_entity(self) -> str:
        """str: The tagging entity part of the tag.

        Example:
            >>> parser = TagUriParser('tag:alice.example.com,2018:Hi')
            >>> parser.tagging_entity
            'alice.example.com,2018'
        """
        return f"{self.authority_name},{self.date}"
    
    @property
    def specific(self) -> str:
        """str: The specific part of a tag URI.

        Examples:
            >>> parser = TagUriParser('tag:alice.example.com,2018:Hi')
            >>> parser.specific
            'Hi'

            >>> parser = TagUriParser('tag:alice.example.com,2018:')
            >>> parser.specific
            ''
        """
        return self.__specific
    
    @property
    def fragment(self) -> str:
        """str: The fragment of an URI, or None if no fragment is given.

        Examples:
            >>> parser = TagUriParser('tag:example.com,2018:Books#Doe')
            >>> parser.fragment
            'Doe'

            >>> parser = TagUriParser('tag:example.com,2018:Books')
            >>> parser.fragment
            None
        """
        return self.__fragment
    
    def tagtuple(self) -> Tuple[str, str, str, str]:
        """A tuple with the extracted parts of the parsed tag.

        This function will return a tuple containing four items, each
        one being a extracted key part of the given tag when
        instantiating this object.

        Returns:
            (str, str, str, str): a tuple containing the authority
                name, date, specific part, and possible fragment.
        """
        return (
            self.authority_name,
            self.date,
            self.specific,
            self.fragment
        )

    def __str__(self):
        return self.__tag