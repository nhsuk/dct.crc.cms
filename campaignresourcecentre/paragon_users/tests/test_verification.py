from unittest.mock import patch
from django.test import TestCase, RequestFactory


class VerificationTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('campaignresourcecentre.paragon_users.views.unsign_user_token')
    def test_verification_input_validation(self, mock_unsign):
        from campaignresourcecentre.paragon_users.views import verification
        
        request = self.factory.get('/verification/')
        response = verification(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
        mock_unsign.return_value = None
        request = self.factory.get('/verification/?q=invalid')
        response = verification(request)
        self.assertEqual(response.status_code, 400)

    @patch('campaignresourcecentre.paragon_users.views.Client')
    @patch('campaignresourcecentre.paragon_users.views.unsign_user_token')
    def test_verification_already_verified_user(self, mock_unsign, mock_client_class):
        from campaignresourcecentre.paragon_users.views import verification
        
        mock_unsign.return_value = 'token'
        mock_client = mock_client_class.return_value
        mock_client.get_user_profile.return_value = {
            'content': {'ProductRegistrationVar2': 'True'}
        }
        
        request = self.factory.get('/verification/?q=token')
        response = verification(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    @patch('campaignresourcecentre.paragon_users.views.render')
    @patch('campaignresourcecentre.paragon_users.views.get_role')
    @patch('campaignresourcecentre.paragon_users.views.Client')
    @patch('campaignresourcecentre.paragon_users.views.unsign_user_token')
    @patch('campaignresourcecentre.paragon_users.views.date')
    def test_verification_success_and_session_handling(self, mock_date, mock_unsign, mock_client_class, mock_get_role, mock_render):
        from campaignresourcecentre.paragon_users.views import verification
        
        mock_date.today.return_value.strftime.return_value = '2023-12-04T10:30:00'
        mock_unsign.return_value = 'token'
        mock_get_role.return_value = 'standard'
        mock_render.return_value = 'response'
        
        mock_client = mock_client_class.return_value
        mock_client.get_user_profile.return_value = {
            'content': {
                'ProductRegistrationVar2': 'False',
                'EmailAddress': 'test@example.com',
                'ContactVar2': 'comms',
                'ProductRegistrationVar4': 'health:nurse'
            }
        }
        mock_client.update_user_profile.return_value = True
        
        request = self.factory.get('/verification/?q=token')
        request.session = {'ParagonUser': 'token'}
        
        verification(request)
        
        self.assertEqual(request.session['Verified'], 'True')
        
        request.session = {'ParagonUser': 'different_token'}
        verification(request)
        self.assertNotIn('Verified', request.session)

    @patch('campaignresourcecentre.paragon_users.views.get_role')
    @patch('campaignresourcecentre.paragon_users.views.Client')
    @patch('campaignresourcecentre.paragon_users.views.unsign_user_token')
    @patch('campaignresourcecentre.paragon_users.views.date')
    def test_verification_update_profile_fails(self, mock_date, mock_unsign, mock_client_class, mock_get_role):
        from campaignresourcecentre.paragon_users.views import verification
        
        mock_date.today.return_value.strftime.return_value = '2023-12-04T10:30:00'
        mock_unsign.return_value = 'token'
        mock_client = mock_client_class.return_value
        mock_client.get_user_profile.return_value = {
            'content': {'ProductRegistrationVar2': 'False', 'EmailAddress': 'test@example.com', 'ContactVar2': 'comms', 'ProductRegistrationVar4': None}
        }
        mock_client.update_user_profile.return_value = False
        
        request = self.factory.get('/verification/?q=token')
        request.session = {}
        response = verification(request)
        
        self.assertEqual(response.status_code, 500)

    def test_verification_job_title_fallback(self):
        from campaignresourcecentre.paragon_users.views import verification
        
        test_cases = [
            {'ContactVar2': 'comms', 'ProductRegistrationVar4': 'health:nurse', 'expected': 'comms'},
            {'ContactVar2': None, 'ProductRegistrationVar4': 'health:nurse', 'expected': 'health:nurse'},
            {'ContactVar2': '', 'ProductRegistrationVar4': 'marketing', 'expected': 'marketing'}
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                with patch('campaignresourcecentre.paragon_users.views.unsign_user_token', return_value='token'), \
                     patch('campaignresourcecentre.paragon_users.views.Client') as mock_client_class, \
                     patch('campaignresourcecentre.paragon_users.views.get_role') as mock_get_role, \
                     patch('campaignresourcecentre.paragon_users.views.date') as mock_date, \
                     patch('campaignresourcecentre.paragon_users.views.render', return_value='response'):
                    
                    mock_date.today.return_value.strftime.return_value = '2023-12-04T10:30:00'
                    mock_client = mock_client_class.return_value
                    mock_client.get_user_profile.return_value = {
                        'content': {
                            'ProductRegistrationVar2': 'False',
                            'EmailAddress': 'test@example.com',
                            'ContactVar2': case['ContactVar2'],
                            'ProductRegistrationVar4': case['ProductRegistrationVar4']
                        }
                    }
                    mock_client.update_user_profile.return_value = True
                    
                    request = self.factory.get('/verification/?q=token')
                    request.session = {}
                    
                    verification(request)
                    
                    mock_get_role.assert_called_once_with('test@example.com', case['expected'])