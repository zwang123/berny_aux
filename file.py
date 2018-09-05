def file_wrapper(file, attr, mode='r', *args, **kwargs):
    """
    A wrapper funtion to deal with files

    file    : input, file name or a file object
    attr    : input, string, the function name to be called
    mode    : opt input, file mode if file is a file name
    rtn     : out, the result returned from attr(*args, **kwargs)
    """
    try:
        rtn = getattr(file, attr)(*args, **kwargs)
    except:
        with open(file, mode) as f:
            rtn = getattr(f, attr)(*args, **kwargs)
    return rtn
