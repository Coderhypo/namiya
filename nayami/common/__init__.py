for m in ['api', 'route']:
    __import__('nayami.%s' % m)

