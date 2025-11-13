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
        test_payload = {"login": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
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
            
            # Test that the result is the expected repos_url from our payload
            expected_url = "https://api.github.com/orgs/test_org/repos"
            self.assertEqual(result, expected_url)


if __name__ == '__main__':
    unittest.main()