from build.lib.django_cache_otp.decorators import skip_if_existsfrom django_cache_otp import generate_otp

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

otp = generate_otp("username", otp_length=6, timeout=60)  # Example: 123456, valid for 60 seconds
is_valid = validate_otp("username", otp)  # Returns True or False
```
if you want to not generate new OTP when username already has one:

```python
otp = generate_otp("username", otp_length=6, timeout=60, skip_if_exists=True)
# return None if username already has an OTP
```


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
