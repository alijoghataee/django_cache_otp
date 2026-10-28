# django-cache-otp

A simple Django package for generating and validating OTPs using Django's cache framework.

## Table of Contents
- [Installation](#installation)
- [Setup](#setup)
  - [Configure Cache (Using Redis)](#configure-cache-using-redis)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation
Install via pip:

```bash
pip install django-cache-otp
```

# Setup
### Configure Cache (Using Redis)
set up your cache settings `settings.py`:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

## Usage
```python
from django_cache_otp import generate_otp, validate_otp

otp = generate_otp("username", otp_length=6, timeout=60)  # Example: "012345", valid for 60 seconds
is_valid = validate_otp("username", otp)  # Returns True or False
```
The OTP is a string, so leading zeros are kept.

if you want to not generate new OTP when username already has one:

```python
otp = generate_otp("username", otp_length=6, timeout=60, skip_if_exists=True)
# return None if username already has an OTP
```

### Rate limiting
`generate_otp` takes `rate_limit` (seconds, default `60`): the minimum time between generating OTPs for the same username. A call made sooner returns `None`.

```python
otp = generate_otp("username", rate_limit=120)  # at most one OTP per 2 minutes
```

`validate_otp` takes two options:
* `rate_limit` (seconds, default `5`): the minimum time between attempts. An attempt made sooner returns `False` without being checked.
* `invalid_after_failure` (count, default `3`): the OTP is invalidated after this many failed attempts. A new OTP has to be generated after that.

```python
is_valid = validate_otp("username", otp, rate_limit=5, invalid_after_failure=3)
```

Pass `0` to any of these options to disable it.


## Features
* Easy integration with Django's cache framework.
* Customizable OTP length and timeout.
* Supports various cache backends (e.g., Redis, Memcached).
* Using SECRET_KEY for encrypt otp.

## Contributing
Contributions are very welcome! Please follow these steps:

* Fork the repository.
* Create a new branch (git checkout -b feature/YourFeature).
* Make your changes and commit them (git commit -m 'Add some feature').
* Push to the branch (git push origin feature/YourFeature).
* Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
