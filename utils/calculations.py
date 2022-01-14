def nextpow2(p):
    """Returns the next power of two

    Returns the smallest power of two that is greater than or equal to the value of p

    Parameters
    ----------
    p
        given number

    Returns
    -------
    n
        the smallest power of two meeting the conditions
    """

    n = 2
    while n < p:
        n *= 2
    return n
