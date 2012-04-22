from july.cache import cache


def test_cache():
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'

    cache.set('key1', 'value2')
    assert cache.get('key1') == 'value2'

    assert cache.add('key1', 'value1') == 'value2'
    assert cache.add('key2', 'value1') == 'value1'

    cache.delete('key1')
    assert cache.get('key1') is None

    mapping = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    cache.set_multi(mapping)
    assert cache.get_multi(['key1', 'key2', 'key3']) == mapping

    cache.delete_multi(['key1', 'key2', 'key3'])

    cache.set_multi(mapping)
    value = cache.get_multi(['1', '2', '3'], key_prefix='key')
    assert value == {'1': 'value1', '2': 'value2', '3': 'value3'}

    cache.flush_all()
    assert cache.get('key1') is None
