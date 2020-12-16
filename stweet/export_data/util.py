"""Utils of export_data methods."""


def clear_file(filename: str):
    """Method to clean file."""
    open(filename, 'w').close()
