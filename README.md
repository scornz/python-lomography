<h1 align="left">python-lomography</h1>

<p align="left">
  <img src="https://cdn.www.lomography.com/assets/api/logo-ac310f0ef22df1894e433d8e6404fac73101518e2a8bc2320a15b91457d8de05.png" />
</p>
<p>
  <a href="https://github.com/scornz/python-lomography/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://github.com/scornz" target="_blank">
    <img alt="Github" src="https://img.shields.io/badge/GitHub-@scornz-blue.svg" />
  </a>
  <a href="https://github.com/scornz" target="_blank">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/scornz/python-lomography">
  </a>
</p>

> A Python SDK for fetching images from the lomography.com API.

## Install

> pip install python-lomography

## Example Usage

For most use cases:

```python
lomo = Lomography(api_key="api_key_here")
photos = lomo.fetch_popular_photos(amt=15)
lomo.close()
```

or for asynchronous use cases:

```python
async_lomo = AsyncLomography(api_key="api_key_here")
photos = await async_lomo.fetch_popular_photos(amt=15)
await async_lomo.close()
```

## Documentation

All documentation for _python-lomography_ can be found [here](https://python-lomography.readthedocs.io/en/latest/).

## Development Requirements

- Python ^3.10 ([download](https://www.python.org/downloads/))
- `poetry` (via [your preferred method](https://python-poetry.org/docs/))
- `make`(hopefully already on your device)

## Setup

1.  Ensure requirements are installed correctly.
2.  Navigate to project folder.
3.  From root folder, call `make`. This should set up all git hooks and install the necessary packages via `poetry`.
4.  Call `poetry run pytest` to ensure that everything is set up correctly. All tests should pass.

## License

Copyright © 2024 [Mike Scornavacca](https://github.com/scornz).<br />
This project is [MIT](https://github.com/scornz/python-lomography/blob/main/LICENSE) licensed.
