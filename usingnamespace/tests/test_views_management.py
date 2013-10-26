import unittest
from pyramid import testing

class ManagementViewsTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def makeOne(self, context, request):
        from usingnamespace.views.management import Management

        return Management(context, request)

    def makeWithInfo(self):
        self.request = testing.DummyRequest()
        self.context = testing.DummyResource()
        self.request.context = self.context

        return self.makeOne(self.context, self.request)

    def test_verify_context_request(self):
        view_class = self.makeOne("1", "2")

        self.assertEqual(view_class.context, "1")
        self.assertEqual(view_class.request, "2")

    def test_management_home(self):
        view_class = self.makeWithInfo()

        self.assertEqual(view_class.home(), {})

class ManagementNotAuthorizedViewsTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = None
        self.context = None

    def tearDown(self):
        testing.tearDown()

    def makeOne(self, context, request):
        from usingnamespace.views.management import ManagementNotAuthorized
        return ManagementNotAuthorized(context, request)

    def makeWithInfo(self):
        self.request = testing.DummyRequest()
        self.context = testing.DummyResource()
        self.request.context = self.context

        return self.makeOne(self.context, self.request)

    def test_view_forbidden(self):
        from pyramid.httpexceptions import HTTPForbidden

        view_class = self.makeWithInfo()
        self.assertRaises(HTTPForbidden, view_class.management_not_authed)

    def test_view_not_found(self):
        view_class = self.makeWithInfo()

        view_class.management_not_found()

        self.assertEqual(self.request.response.status_int, 404)
