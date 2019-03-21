# anschluss

[![CircleCI Build](https://circleci.com/gh/westnetz/anschluss.svg?style=shield)](https://circleci.com/gh/westnetz/anschluss "CircleCI Build")
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://renovateapp.com/ "Renovate enabled")

This is a Django project implementing the westnetz order form.

## Development

For local development, first create a virtualenv:

```console
python -m venv venv
```

Afterwards, setup git-flow and install all dependencies using:

```console
make develop
```

For development, use django runserver to run the application locally:

```console
./manage.py runserver
```

## Contributing changes

This project uses git-flow. To contribute changes, create a feature branch
based on `develop` and work on your changes there.

To test your changes locally, you can run:

```console
make check
```

Once you are finished, publish the branch and open a pull-request for review.
