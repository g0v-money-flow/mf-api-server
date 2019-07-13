from graphene import ObjectType, String, Int, Boolean, Float, List, Field
from common.dataLoader.dataLoader import get_all_election, get_election, get_regions
from common.model.financeData import INCOME_CATEGORY, OUTCOME_CATEGORY


class FinanceCategoryItem(ObjectType):
    name = String()
    amount = Int()
    item_count = Int()


class FinanceOutcomeItem(ObjectType):
    total = Int()
    items = List(FinanceCategoryItem)

    def resolve_items(parent, info):
        return parent.getRecords(OUTCOME_CATEGORY)['items']


class FinanceIncomeItem(ObjectType):
    total = Int()
    items = List(FinanceCategoryItem)

    def resolve_items(parent, info):
        return parent.getRecords(INCOME_CATEGORY)['items']


class Finance(ObjectType):
    income = Field(FinanceIncomeItem)
    outcome = Field(FinanceOutcomeItem)

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
    detail_link = String()
    id = Int()

    def resolve_finance(parent, info):
        return parent.finance_data


class Constituency(ObjectType):
    id = String()
    name = String()
    candidates = List(Candidate)

    def resolve_candidates(parent, info):
        return parent['instance'].get_candidates()


class Region(ObjectType):
    name = String()
    constituencies = List(Constituency)

    def resolve_constituencies(parent, info):
        return parent['constituencies'].values()


class Election(ObjectType):
    name = String()
    e_type = String()
    year = Int()
    regions = List(Region)

    def resolve_regions(parent, info):
        return get_regions(parent)


class Query(ObjectType):
    election = Field(Election, etype=String(
        required=True), year=Int(required=True))
    all = List(Election)
    candidate = Field(Candidate, name=String(required=True))

    def resolve_election(self, info, etype, year):
        return get_election(etype, str(year))

    def resolve_all(self, info):
        return get_all_election()
