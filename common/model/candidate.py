from .region import Region
from .party import Party
from .person import Person


class Candidate:
    # class member
    id_counter = 0

    # object member
    id: int
    region: Region
    party: Party
    person: Person
    vice: Person
    is_elected: bool
    num_of_vote: int
    rate_of_vote: float

    @classmethod
    def generateId(cls):
        cls.id_counter += 1
        tmp = cls.id_counter
        return tmp

    def __init__(self, region, person, party, is_elected):
        self.id = Candidate.generateId()
        self.region = region
        self.person = person
        self.party = party
        self.is_elected = is_elected
        self.vice = None
        self.finance_data = None

    @property
    def name(self):
        return self.person.name

    @property
    def party_name(self):
        return self.party.name

    @property
    def vice_candidate(self):
        if self.vice is None:
            return None
        else:
            return self.vice.name

    def set_vice_candidate(self, person):
        self.vice = person

    def set_result(self, num_of_vote, rate_of_vote):
        self.num_of_vote = num_of_vote
        self.rate_of_vote = rate_of_vote

    def set_finance_data(self, finance_data):
        self.finance_data = finance_data
