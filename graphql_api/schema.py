from graphene import ObjectType, String, Int, Boolean, Float, List, Field

from common.data_loader import get_election, get_regions

class FinanceCategoryItem(ObjectType):
    name = String()
    amount = Int()

class FinanceItem(ObjectType):
    total = Int()
    items = List(FinanceCategoryItem)

    def resolve_items(parent, info):
        return parent.items

class Finance(ObjectType):
    income = Field(FinanceItem)
    outcome = Field(FinanceItem)

    def resolve_income(parent, info):
        return parent.income_records

    def resolve_outcome(parent, info):
        return parent.outcome_records

class Candidate(ObjectType):
    name = String()
    party_name = String()
    vice_candidate = String()
    is_elected = Boolean()
    num_of_vote = Int()
    rate_of_vote = Float()
    finance = Field(Finance)

    def resolve_finance(parent, info):
        return parent.finance_data

class Constitution(ObjectType):
    name = String()
    candidates = List(Candidate)

    def resolve_candidates(parent, info):
        return parent['instance'].get_candidates()

class Region(ObjectType):
    name = String()
    constitutions = List(Constitution)

    def resolve_constitutions(parent, info):
        return parent['constitutions'].values()

class Election(ObjectType):
    name = String()
    regions = List(Region)

    def resolve_regions(parent, info):
        return get_regions(parent)

class Query(ObjectType):
    election = Field(Election, etype = String(required = True), year = Int(required = True))
    def resolve_election(self, info, etype, year):
        return get_election(etype, str(year))

