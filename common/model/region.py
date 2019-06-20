class Region:
    region_code: str
    name: str
    city: dict

    def __init__(self, code, name, city):
        self.region_code = code
        self.name = name
        self.candidates = {}
        self.city = city

    def put_candidate(self, number, candidate):
        self.candidates[number] = candidate

    def get_candidate(self, number):
        if number in self.candidates:
            return self.candidates[number]
        else:
            return None

    def get_candidates(self):
        return self.candidates.values()
