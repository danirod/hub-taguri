from unittest import TestCase

from taguri.parser import TagUriParser

class TagUriParserTestCase(TestCase):

    def test_behaviour_of_parser(self):
        given = 'tag:alice.example.org,2018-11-22:Books/Book'
        parser = TagUriParser(given)
        self.assertEqual('alice.example.org', parser.authority_name)
        self.assertEqual('2018-11-22', parser.date)
        self.assertEqual('alice.example.org,2018-11-22', parser.tagging_entity)
        self.assertEqual('Books/Book', parser.specific)
        self.assertEqual(None, parser.fragment)

    def test_behaviour_of_parser_with_fragment(self):
        given = 'tag:alice.example.org,2018-11-22:Collections/Books#Doe'
        parser = TagUriParser(given)
        self.assertEqual('alice.example.org', parser.authority_name)
        self.assertEqual('2018-11-22', parser.date)
        self.assertEqual('alice.example.org,2018-11-22', parser.tagging_entity)
        self.assertEqual('Collections/Books', parser.specific)
        self.assertEqual('Doe', parser.fragment)
    
    def test_parser_accepts_empty_specific(self):
        parser = TagUriParser('tag:alice.example.org,2018-11-22:')
        self.assertEqual('', parser.specific)
        
    def test_parser_fails_on_invalid_tags(self):
        test_cases = (
            'hello.example.com',
            'hello.example.com,2018',
            'hello.example.com,2018:Book',
            'hello.example.com,2018:Book#Doe',
            'tag:comma,example.com,2017:InvalidComma',
            'tag:hello.example.com:LacksDate',
            'tag:hello.example.com', # lacks specific
            'tag:hello.example.com#lacks-specific-too',
            'tag:2018:LacksDomain',
            'tag:',
        )
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with self.assertRaises(AttributeError):
                    TagUriParser(test_case)