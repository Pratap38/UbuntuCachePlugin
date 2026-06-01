def bytes_to_mb(size_in_bytes):

    return size_in_bytes / (1024 * 1024)


def bytes_to_gb(size_in_bytes):

    return size_in_bytes / (1024 * 1024 * 1024)


def format_size(size_in_bytes):

    gb = bytes_to_gb(size_in_bytes)

    if gb >= 1:

        return f"{gb:.2f} GB"

    mb = bytes_to_mb(size_in_bytes)

    return f"{mb:.2f} MB"