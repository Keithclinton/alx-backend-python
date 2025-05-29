#!/usr/bin/env python3
"""
Unit test for GithubOrgClient.has_license
"""

import unittest
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license correctly checks the license key"""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.has_license(repo, license_key), expected)
