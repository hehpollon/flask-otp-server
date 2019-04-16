# flask-otp-server
Simple OTP server using [pyotp](https://github.com/pyauth/pyotp).<br>
Supports HOTP([RFC 4226](https://tools.ietf.org/html/rfc4226)) / TOTP([RFC 6238](https://tools.ietf.org/html/rfc6238)).<br>
Using database [tinydb](https://github.com/msiemens/tinydb).

## Installation
```
pip3 install -r requirements.txt
```

## Run
```
$ python3 main.py
```
> server should run with ssl

## API
### - generate otp
#### request:
```
/generate?user_id=test@test.com&algorithm=totp
```
#### response:
```
{ 
    "provisioning_uri":"otpauth://totp/flask-otp-server:test%40test.com?secret=FDDM2IOYWXTV4P53&issuer=flask-otp-server",
    "secret_key":"FDDM2IOYWXTV4P53"
}
```
### - verify otp
#### request:
```
/verify?user_id=test@test.com&algorithm=totp&otp_value=384291
```
#### response:
```
{
    "result": "True"
}
```

## Contributing

This is an open source project so feel free to contribute by

- Opening an [issue](https://github.com/hehpollon/flask-otp-server/issues/new)
- Sending me feedback via [email](mailto://hehpollon@gmail.com)
