from rest_framework import status
from rest_framework.permissions import SAFE_METHODS

import pytest


class ListViewTestCasePermissionsMixin:
    """ Provides permissions-related tests for list views """

    @pytest.mark.parametrize("method", ['get', 'head', 'options', 'post'])
    def test_request_with_admin_check_can_make_requests_with_all_methods(
        self, admin_user, client, method
    ):
        client.login(username="admin", password="password")

        response = getattr(client, method)(self.URL)
        assert response.status_code != status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("method", ['get', 'head', 'options', 'post'])
    def test_request_with_anonymous_user_check_can_make_requests_with_safe_but_not_unsafe_methods(
        self, client, method
    ):
        if method.upper() in SAFE_METHODS:
            response = getattr(client, method)(self.URL)
            assert response.status_code != status.HTTP_403_FORBIDDEN
        else:
            response = getattr(client, method)(self.URL)
            assert response.status_code == status.HTTP_403_FORBIDDEN


class DetailViewTestCasePermissionsMixin:
    """ Provides permissions-related tests for detail views """

    @pytest.mark.parametrize("method", ['get', 'head', 'options', 'put', 'patch',
                                        'delete'])
    def test_request_with_admin_check_can_make_requests_with_all_methods(
        self, admin_user, client, method
    ):
        client.login(username="admin", password="password")
        response = getattr(client, method)(self.URL)
        assert response.status_code != status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("method", ['get', 'head', 'options', 'put', 'patch',
                                        'delete'])
    def test_request_with_anonymous_user_check_can_make_requests_with_safe_but_not_unsafe_methods(
        self, client, method
    ):
        if method.upper() in SAFE_METHODS:
            response = getattr(client, method)(self.URL)
            assert response.status_code != status.HTTP_403_FORBIDDEN
        else:
            response = getattr(client, method)(self.URL)
            assert response.status_code == status.HTTP_403_FORBIDDEN

