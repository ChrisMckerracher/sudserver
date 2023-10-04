from redis import Redis


def get_client() -> Redis:
    #toDO: hardcode now, real stuff lata
    return Redis(host='localhost', port=6379, decode_responses=True)