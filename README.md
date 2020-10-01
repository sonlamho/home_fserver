# home_fserver

### Security details
- Set your password by running `python home_fserver/utils.py --set-pass`. The hash+salt of the sha256 hash of your password will be saved to a file. Yes we are hashing twice here.
- Generate a key for your server with `python home_fserver/utils.py --generate-key`
- When you log in, the password is immediately hashed (sha256) in browser, then that hash is sent to the server to be checked with the saved hash+salt.
- Unless running only on LAN or you know what you're doing, you should always deploy the server with https only. Sending infos without TLS (https) will make your server accessible to other people on the internet.

### Deployment instructions
(Work in progress)
