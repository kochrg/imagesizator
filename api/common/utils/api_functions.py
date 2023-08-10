def diff_month(d1, d2):
    # Get months between two dates. D2 <= D1
    if d1 == d2:
        return 0
    return (d1.year - d2.year) * 12 + d1.month - d2.month
