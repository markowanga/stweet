"""Utils of export methods."""


def clear_file(filename: str):
    """Method to clean file."""
    open(filename, 'w').close()
