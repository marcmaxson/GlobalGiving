api_key = 'ENTER YOUR API KEY HERE'
# you can request an API key at https://www.globalgiving.org/dy/v2/developer/get-api-key.html

class gg:
    # by default, everything comes back as json, not xml.
    def __init__(self, api_key):
        self.api_key = api_key

    def parse_json(self, D):
        for k, v in D.items():
            if type(v) in (list, tuple, dict):
                pass
            if isinstance(v, dict):
                for id_val in self.parse_json(v):
                    yield id_val
            elif isinstance(v, list):
                for i in v:
                    if isinstance(i, dict):
                        for id_val in self.parse_json(i):
                            yield id_val

    def save_pretty_json(self, D, filename):
        import json
        for _ in self.parse_json(D):
            pretty = json.dumps(_, sort_keys=True, indent=2, separators=(',', ': '))
            with open(filename, 'w') as f:
                f.write(pretty)

    # not working yet
    # def text_from_json(self, D):
    #     text = ''
    #     for d in self.parse_json(D):
    #         # if not isinstance(d, dict):
    #         text += self.no_tags(d)
    #         # else:
    #         #    text += no_tags(str(d.values()))
    #     return text

    def no_tags(self, data):
        """ returns string without any html / xml tags using r'<.*?>' pattern to match
        also strips any latin1 escaped characters starting with r'\\x' """
        try:
            import re
            p = re.compile(r'<.*?>') # strip <...> out
            x = re.compile(r'\\x') # strip unicode \x...
            data = x.sub('', data)
            return p.sub('', data)
        except Exception as e:
            import logging
            log_filename = 'error.log'
            logging.basicConfig(filename=log_filename, level=logging.DEBUG)
            logging.exception(str(e))
            return '' # empty string?

    def project_info_from_ids(self, project_id_list, print_url=False):
        """Query String Parameters:
            &api_key described in the API Key section, required
            &projectIds a comma separated list of project ids (maximum of 10 ids), required
            Query String Example:
            api/public/projectservice/projects/collection/ids?api_key=YOUR_API_KEY&projectIds=123,1883
            USEFUL: len(x.json()['projects']['project']) -- number of projects returned
            #resp = requests.get('https://api.globalgiving.org/api/public/projectservice/projects/collection/ids?projectId=[1885,2221,14722,8536,6977,12312,14721]&api_key=3a11f6e4-5c07-49cf-abe5-e7b4c09fc500')
        """
        import requests
        from urllib import urlencode, unquote
        url = 'https://api.globalgiving.org/api/public/projectservice/projects/collection/ids'
        # True unpacks lists the wrong way for api. need to hack it. Note: MAX 10 ids
        ids = str(project_id_list[:10])[1:-1].replace(' ', '')
        params = urlencode({'api_key': self.api_key, 'projectIds': ids})
        json = {"Accept": "application/json"}
        if print_url:
            print unquote(url + '?' + params)
        resp = requests.get(url + '?' + params, headers=json)
        return resp

    def project_info_from_org_id(self, org_id, active_only=True, print_url=False):
        """
        TIP: Adding '/active' to the path returns only active projects able to accept donations. Funded and retired projects are excluded.
        NOTE: The <project> element is repeating.
        """
        import requests
        from urllib import urlencode, unquote
        url = 'https://api.globalgiving.org/api/public/projectservice/organizations/%s/projects' % org_id
        params = urlencode({'api_key': self.api_key})
        if active_only is True:
            url += '/active'
        json = {"Accept":"application/json"}
        if print_url:
            print unquote(url + '?' + params)
        resp = requests.get(url + '?' + params, headers=json)
        return resp

    def atom_reports_from_project_id(self, project_id, use='xml', print_url=False):
        # see http://www.globalgiving.org/api/get-progress-report-for-a-specific-project.html
        import requests
        from urllib import urlencode, unquote
        url = 'https://api.globalgiving.org/api/public/projectservice/projects/%s/reports' % project_id
        params = urlencode({'api_key': self.api_key})
        if use == 'json':
            content_type = {"Accept": "application/json"}
        else:
            content_type = ''
        if print_url:
            print unquote(url + '?' + params)
        resp = requests.get(url + '?' + params, headers=content_type)
        return resp

    def get_org(self, org_id, use='json', print_url=False):
        import requests
        from urllib import urlencode, unquote
        url = 'https://api.globalgiving.org/api/public/orgservice/organization/%s' % org_id
        params = urlencode({'api_key':self.api_key})
        if use == 'json':
            json = {"Accept": "application/json"}
        else:
            json = {"Accept": "application/xml"}
        if print_url:
            print unquote(url + '?' + params)
        resp = requests.get(url + '?' + params,headers=json)
        return resp
