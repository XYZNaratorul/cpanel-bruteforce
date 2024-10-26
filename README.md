### About 


This brute forcing script is made to target HTTP Basic Authentication login panels, not just cpanel.
The script can only work with panels that respond with a 401 Unauthorized error when incorrect credentials are supplied.
However, you can modify the script to work with other types of login panels, depending on the authentication mechanism they use. 

* Example:

### Form-Based Authentication

```
data = urllib.parse.urlencode({'username': u, 'password': p}).encode()
req = urllib.request.Request(login_url, data=data)
```
* you can see the help menu by running

```
python bruteforce.py
```
