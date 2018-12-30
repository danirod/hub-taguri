from unittest import mock, TestCase
from taguri.minter import TagUriMinter

class TagUriMinterTestCase(TestCase):

    @mock.patch('taguri.minter.authority_name_validator', return_value=True)
    def test_minter_validates_authority_name(self, validator):
        TagUriMinter('example.org', '2018')
        self.assertTrue(validator.called)
        self.assertTupleEqual(('example.org',), validator.call_args[0])
    
    @mock.patch('taguri.minter.date_validator', return_value=True)
    def test_minter_validates_date(self, validator):
        TagUriMinter('example.org', '2018-11-21')
        self.assertTrue(validator.called)
        self.assertTupleEqual(('2018-11-21',), validator.call_args[0])
    
    @mock.patch('taguri.minter.authority_name_validator', return_value=False)
    def test_minter_raises_if_authority_name_is_not_valid(self, validator):
        with self.assertRaises(AttributeError):
            TagUriMinter('whatever', '2018')
    
    @mock.patch('taguri.minter.date_validator', return_value=False)
    def test_minter_raises_if_date_is_not_valid(self, validator):
        with self.assertRaises(AttributeError):
            TagUriMinter('example.com', '2018-11-21')
    
    def test_minter_properties(self):
        minter = TagUriMinter('alice.example.org', '2018-11-21')
        self.assertEqual('alice.example.org', minter.authority_name)
        self.assertEqual('2018-11-21', minter.date)
        self.assertEqual('alice.example.org,2018-11-21', minter.tagging_entity)
        self.assertEqual('tag:alice.example.org,2018-11-21', minter.prefix)
    
    def test_minter_mints(self):
        minter = TagUriMinter('alice.example.org', '2018-11-21')
        expected = 'tag:alice.example.org,2018-11-21:Collections/Books'
        self.assertEqual(expected, minter.mint('Collections/Books'))
    
    def test_minter_mints_with_fragment(self):
        minter = TagUriMinter('alice.example.org', '2018-11-21')
        expected = 'tag:alice.example.org,2018-11-21:Collections/Books#Doe'
        self.assertEqual(expected, minter.mint('Collections/Books', 'Doe'))
    
    @mock.patch('taguri.minter.specific_validator', return_value=False)
    def test_minter_raises_if_specific_is_not_valid(self, validator):
        with self.assertRaises(AttributeError):
            minter = TagUriMinter('alice.example.org', '2018-11-21')
            minter.mint('Invalid/Item')
        self.assertEqual(1, validator.call_count)
        
    @mock.patch('taguri.minter.specific_validator', side_effect=(True, False))
    def test_minter_raises_if_fragment_is_not_valid(self, validator):
        with self.assertRaises(AttributeError):
            minter = TagUriMinter('alice.example.org', '2018-11-21')
            minter.mint('Invalid/Item', 'DoeFragment')
        self.assertEqual(2, validator.call_count)