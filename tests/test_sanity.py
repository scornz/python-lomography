from lomography import __version__


def test_version():
    """Test the version of the package. This is simply here to make sure that
    version changes are purposeful and consistent."""

    assert __version__ == "0.1.0"
