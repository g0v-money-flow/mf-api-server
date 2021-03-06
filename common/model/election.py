class Election:
    def __init__(self, e_type, year):
        self.e_type = e_type
        self.year = int(year)
        self.city_db = {}
        self.region_db = {}
        self.party_db = {}
        self.cand_db = {}

    @property
    def name(self):
        return '{} {} Election'.format(self.year, str.capitalize(self.e_type))

    def get_city_list(self):
        return [{
            'name': city,
            'head_code': sorted(list(regions.keys()))[0]
        } for city, regions in self.city_db.items()]

    def get_region_list(self):
        return [{'id': k, 'name': str(v)} for k, v in self.region_db.items() if v.has_candidate()]

    def get_region(self, id):
        if id in self.region_db:
            return self.region_db[id]
        else:
            return None

    def get_candidate_list(self):
        return self.cand_db.values()

    def get_candidate(self, id):
        if id in self.cand_db:
            return self.cand_db[id]
        else:
            return None
