from unittest import TestCase
from taguri.validator import (
    authority_name_validator,
    date_validator,
    specific_validator,
)

class AuthorityNameValidatorTestCase(TestCase):
    def test_accepts_domain_names(self):
        test_cases = (
            'unqualified-domain-name',
            'fully-qualified-domain-name.local',
            'fully-qualified-domain-name.com',
            'example.org',
            'subdomain.example.org',
            '1leadingnumber',
            'trailingnumber2',
        )
        for test_case in test_cases:
            with self.subTest(email=test_case):
                self.assertTrue(authority_name_validator(test_case),
                                '{} should be valid'.format(test_case))
    
    def test_rejects_invalid_domain_names(self):
        test_cases = (
            '.no-leading-dots',
            'no-trailing-dots.',
            '-no-leading-dashes',
            'no-leading-dashes-',
            '', # no empty strings
            'no:colons',
            'no/slashes',
            'no,commas',
            'no!weird!characters',
        )
        for test_case in test_cases:
            with self.subTest(email=test_case):
                self.assertFalse(authority_name_validator(test_case),
                                 '{} should not be valid'.format(test_case))

    # https://blogs.msdn.microsoft.com/testing123/2009/02/06/email-address-test-cases/
    # Note, however, that there are cases left out because the tag URI
    # grammar allows or disallows so.

    def test_accepts_mail_addresses(self):
        test_cases = (
            'email@example.com',
            'firstname.lastname@example.com',
            'email@subdomain.example.com',
            'firstname+lastname@example.com',
            'email@123.123.123.123',
            # 'email@[123.123.123.123]', # DNSname does not allow brackets
            # '"email"@example.com', # emailAddress does not allow quotes
            '1234567890@example.com',
            'email@example-one.com',
            '_______@example.com',
            'email@example.name',
            'email@example.museum',
            'email@example.co.jp',
            'firstname-lastname@example.com',
        )
        for test_case in test_cases:
            with self.subTest(email=test_case):
                self.assertTrue(authority_name_validator(test_case),
                                '{} should be valid'.format(test_case))
    
    def test_rejects_invalid_mail_addresses(self):
        test_cases = (
            # 'plainaddress', # will be parsed as a DNSname instead.
            '#@%^%#$@#$@#.com',
            '@example.com',
            'Joe Smith <email@example.com>',
            'email@example@example.com',
            # '.email@example.com', # emailAddress allow leading dots
            # 'email.@example.com', # emailAddress allow trailing dots
            # 'email..email@example.com', # emailAddress allow consecutive dots
            'あいうえお@example.com',
            'email@example.com (Joe Smith)',
            # 'email@example', # DNSname allows unqualified domain names
            'email@-example.com',
            # 'email@example.web', # DNSname doesn't test TLDs.
            # 'email@111.222.333.44444', # DNSname is lax enough to allow this.
            'email@example..com',
            # 'Abc..123@example.com', # emailAddrress allow consecutive dots
        )
        for test_case in test_cases:
            with self.subTest(email=test_case):
                self.assertFalse(authority_name_validator(test_case),
                                 '{} should not be valid'.format(test_case))

class DateValidator(TestCase):

    def test_accepts_valid_dates(self):
        test_cases = (
            '2018',
            '2018-11',
            '2018-11-26',
            '1999-11',
            '1000-01-01',
            '2999-12-31',
            '9999-12-31',
            '9999',
            '0001-01-01',
        )
        for test_case in test_cases:
            with self.subTest(email=test_case):
                self.assertTrue(date_validator(test_case),
                                '{} should be valid'.format(test_case))
    
    def test_rejects_invalid_dates(self):
        test_cases = (
            'YYYY',
            'YYYY-MM',
            'YYYY-MM-DD',
            '2018-26-11',
            '914-15-16',
            'year',
        )
        for test_case in test_cases:
            with self.subTest(email=test_case):
                self.assertFalse(date_validator(test_case),
                                 '{} should not be valid'.format(test_case))


class SpecificValidatorTestCase(TestCase):

    def test_accepted_tokens(self):
        test_cases = (
            '',
            'specific',
            '123',
            'path/to/resource.html',
            '(hello)',
            'hello%20world',
            '1.Foo.Bar.2',
        )
        for test_case in test_cases:
            with self.subTest(email=test_case):
                self.assertTrue(specific_validator(test_case),
                                '{} should be valid'.format(test_case))
    
    def test_rejected_tokens(self):
        test_cases = (
            '<rejected>',
            '[hello]',
            'hello world',
            '%HF-is-not-pct',
            'watchout-for-the#fragment',
        )
        for test_case in test_cases:
            with self.subTest(email=test_case):
                self.assertFalse(specific_validator(test_case),
                                 '{} should not be valid'.format(test_case))