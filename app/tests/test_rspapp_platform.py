import rsvp
import mongomock
import unittest
import json
from unittest.mock import patch
from bson import ObjectId

class BaseTest(unittest.TestCase):
    def setUp(self):
        rsvp.client = mongomock.MongoClient()
        rsvp.db = rsvp.client.mock_db
        self.client = rsvp.app.test_client()

class TestRSVPModel(BaseTest):
    def test_dict(self):
        doc = rsvp.RSVP("test name", "test@example.com", "507f1f77bcf86cd799439011")
        with rsvp.app.test_request_context():
            result = doc.dict()
        self.assertEqual(result["name"], "test name")
        self.assertEqual(result["email"], "test@example.com")
        self.assertTrue(result["links"]["self"].endswith("/api/rsvps/507f1f77bcf86cd799439011"))

    def test_new_and_find(self):
        doc = rsvp.RSVP.new("test name", "test@example.com")
        self.assertEqual(doc.name, "test name")
        self.assertEqual(doc.email, "test@example.com")
        self.assertIsNotNone(rsvp.RSVP.find_one(doc._id))
        self.assertEqual(len(rsvp.RSVP.find_all()), 1)

    def test_delete(self):
        doc = rsvp.RSVP.new("delete me", "delete@example.com")
        self.assertEqual(len(rsvp.RSVP.find_all()), 1)
        doc.delete()
        self.assertEqual(len(rsvp.RSVP.find_all()), 0)

class TestRSVPRoutes(BaseTest):
    def test_get_rsvps_api_empty(self):
        res = self.client.get("/api/rsvps")
        self.assertEqual(res.status_code, 200)
        self.assertIn("[]", res.data.decode())

    def test_post_rsvp_api_success(self):
        payload = {"name": "John", "email": "john@example.com"}
        res = self.client.post("/api/rsvps", data=json.dumps(payload))
        self.assertEqual(res.status_code, 200)
        self.assertIn("John", res.data.decode())

    def test_post_rsvp_api_missing_fields(self):
        res = self.client.post("/api/rsvps", data=json.dumps({"name": "Jane"}))
        self.assertEqual(res.status_code, 400)
        self.assertIn("email field is missing", res.data.decode())

        res = self.client.post("/api/rsvps", data=json.dumps({"email": "jane@example.com"}))
        self.assertEqual(res.status_code, 400)
        self.assertIn("name field is missing", res.data.decode())

    def test_get_single_rsvp(self):
        doc = rsvp.RSVP.new("Single", "single@example.com")
        res = self.client.get(f"/api/rsvps/{doc._id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Single", res.data.decode())

    def test_delete_rsvp(self):
        doc = rsvp.RSVP.new("Delete", "delete@example.com")
        res = self.client.delete(f"/api/rsvps/{doc._id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Deleted", res.data.decode())

    def test_root_route(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("html", res.data.decode())

    def test_new_form_route(self):
        res = self.client.post("/new", data={"name": "Web", "email": "web@example.com"})
        self.assertEqual(res.status_code, 302)  # Redirect expected

if __name__ == "__main__":
    unittest.main()
