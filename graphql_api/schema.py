from graphene import ObjectType, String, Int, List, Field

class Candidate(ObjectType):
    name = String()

class Constitution(ObjectType):
    name = String()
    candidates = List(Candidate)

    def resolve_candidates(self, info):
        return [{'name': 'abc'}, {'name': 'dde'}]

class Region(ObjectType):
    name = String()
    constitutions = List(Constitution)

    def resolve_constitutions(self, info):
        return [{'name': '01'}, {'name': '02'}]

class Election(ObjectType):
    name = String()
    regions = List(Region)

    def resolve_regions(self, info):
        return [{'name': 'taipei'}, {'name': 'hsinchu'}]

class Query(ObjectType):
    election = Field(Election, etype = String(required = True), year = Int(required = True))
    def resolve_election(self, info, etype, year):
        return {'name': '{} {} Election'.format(year, str.capitalize(etype))}

