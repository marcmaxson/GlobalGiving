with open('api.key','r') as f: # a local file not in repo
    api_key = f.read()

def test_get_org(api_key):
    from gg_api import gg    
    GG = gg(api_key)
    resp = GG.get_org(754)
    resp = resp.json()
    assert resp['organization']['name'] == 'Vijana Amani Pamoja (VAP)'
    print('ok')
