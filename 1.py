def get_query_results(*filters):
    res = models.Item.query
    for i, filt in enumerate(filters, 1):
        if filt is not None:
            d = {'filter{}'.format(i): filt}
            res = res.filter(**d)
    return res.all()

