#!/usr/bin/env python3
"""
Unit tests for client module
"""
import unittest
from parameterized import parameterized, parameterized_class
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test that GithubOrgClient.has_license returns the expected boolean
        """
        # Call the static method directly (no instance needed)
        result = GithubOrgClient.has_license(repo, license_key)

        # Test that the result matches the expected boolean
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        'org_payload': None,  # Will be set from fixtures
        'repos_payload': None,  # Will be set from fixtures  
        'expected_repos': None,  # Will be set from fixtures
        'apache2_repos': None,  # Will be set from fixtures
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for client.GithubOrgClient
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class method to mock requests.get for integration testing
        """
        # Import fixtures
        from fixtures import TEST_PAYLOAD
        
        # Extract fixtures from TEST_PAYLOAD
        cls.org_payload = TEST_PAYLOAD[0][0]
        cls.repos_payload = TEST_PAYLOAD[0][1]
        cls.expected_repos = TEST_PAYLOAD[0][2]
        cls.apache2_repos = TEST_PAYLOAD[0][3]
        
        # Define side_effect function to return appropriate payload based on URL
        def get_side_effect(url):
            """Side effect function to return appropriate payload based on URL"""
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data
                
                def json(self):
                    return self.json_data
            
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload['repos_url']:
                return MockResponse(cls.repos_payload)
            return MockResponse({})

        # Start patcher for requests.get
        cls.get_patcher = patch('requests.get', side_effect=get_side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class method to stop the patcher
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Integration test for GithubOrgClient.public_repos
        """
        # Create client instance
        client = GithubOrgClient("google")
        
        # Call public_repos method
        result = client.public_repos()
        
        # Test that the result matches expected_repos from fixtures
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Integration test for GithubOrgClient.public_repos with license filter
        """
        # Create client instance
        client = GithubOrgClient("google")
        
        # Call public_repos method with apache-2.0 license filter
        result = client.public_repos("apache-2.0")
        
        # Test that the result matches apache2_repos from fixtures
        self.assertEqual(result, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()