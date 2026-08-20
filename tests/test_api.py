class TestRootEndpoint:
    def test_root(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json()["message"] == "Contact Form API is running"


class TestHealthEndpoint:
    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"


class TestContactEndpoint:
    def test_success(self, client, valid_form_data):
        resp = client.post("/api/contact", json=valid_form_data)
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        assert body["telegram_sent"] is True

    def test_validation_error_empty_name(self, client, valid_form_data):
        valid_form_data["name"] = ""
        resp = client.post("/api/contact", json=valid_form_data)
        assert resp.status_code == 400

    def test_validation_error_short_message(self, client, valid_form_data):
        valid_form_data["message"] = "短い"
        resp = client.post("/api/contact", json=valid_form_data)
        assert resp.status_code == 400

    def test_invalid_email(self, client, valid_form_data):
        valid_form_data["email"] = "bad-email"
        resp = client.post("/api/contact", json=valid_form_data)
        assert resp.status_code == 422

    def test_missing_body(self, client):
        resp = client.post("/api/contact")
        assert resp.status_code == 422
