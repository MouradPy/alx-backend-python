#!/usr/bin/env python3
"""
Unit tests for client module
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for client.GithubOrgClient
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument
        """
        # Set up the mock return value
        test_payload = {
            "login": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = test_payload

        # Create GithubOrgClient instance
        client = GithubOrgClient(org_name)

        # Call the org property (not method!)
        result = client.org

        # Test that get_json was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Test that the result matches the mock return value
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the expected value
        """
        # Test payload with known repos_url
        test_payload = {
            "login": "test_org",
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        # Patch GithubOrgClient.org property to return our test payload
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock,
                   return_value=test_payload) as mock_org:
            # Create GithubOrgClient instance
            client = GithubOrgClient("test_org")

            # Call the _public_repos_url property
            result = client._public_repos_url

            # Test that the result is the expected repos_url
            expected_url = "https://api.github.com/orgs/test_org/repos"
            self.assertEqual(result, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns expected list of repos
        """
        # Test payload for repos
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        mock_get_json.return_value = test_repos_payload

        # Expected repository names
        expected_repos = ["repo1", "repo2", "repo3"]

        # Mock _public_repos_url to return a test URL
        test_url = "https://api.github.com/orgs/test_org/repos"
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock,
                   return_value=test_url) as mock_public_repos_url:

            # Create GithubOrgClient instance
            client = GithubOrgClient("test_org")

            # Call public_repos method
            result = client.public_repos()

            # Test that the list of repos matches expected names
            self.assertEqual(result, expected_repos)

            # Test that _public_repos_url was called once
            mock_public_repos_url.assert_called_once()

            # Test that get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with(test_url)
