class TestBase:

    def login(self, test_client, email, password):
        r = test_client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)
        return r
