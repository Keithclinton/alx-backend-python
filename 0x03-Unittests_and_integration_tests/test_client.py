#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient._public_repos_url
"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    def test_public_repos_url(self):
        """Test the _public_repos_url property"""
        payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}

        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("test-org")
            result = client._public_repos_url

            self.assertEqual(result, payload["repos_url"])
            mock_org.assert_called_once()
