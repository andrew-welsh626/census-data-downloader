#! /usr/bin/env python
# -*- coding: utf-8 -*
import collections
from census_data_downloader.core.tables import BaseTableConfig
from census_data_downloader.core.decorators import register


@register
class ClassOfWorkerDownloader(BaseTableConfig):
    """
    Sex by Class of Worker for the Civilian Employed Population 16 Years and Over.
    """
    PROCESSED_TABLE_NAME = "classofworker"
    UNIVERSE = "civilian employed population 16 years and over"
    RAW_TABLE_NAME = 'B24080'
    RAW_FIELD_CROSSWALK = collections.OrderedDict({
        '001': "universe",
        '002': "male_total",
        '003': "male_private_for_profit_wage_and_salary",
        '004': "male_employee_of_private_company",
        '005': "male_selfemployed_in_own_incorporated_business",
        '006': "male_private_not_for_profit_wage_and_salary",
        '007': "male_local_government",
        '008': "male_state_government",
        '009': "male_federal_government",
        '010': "male_selfemployed_in_own_not_incorporated_business",
        '011': "male_unpaid_family_workers",
        '012': "female_total",
        '013': "female_private_for_profit_wage_and_salary",
        '014': "female_employee_of_private_company",
        '015': "female_selfemployed_in_own_incorporated_business",
        '016': "female_private_not_for_profit_wage_and_salary",
        '017': "female_local_government",
        '018': "female_state_government",
        '019': "female_federal_government",
        '020': "female_selfemployed_in_own_not_incorporated_business",
        '021': "female_unpaid_family_workers"
    })

    def process(self,df):
        df = super().process(*args, **kwargs)

        # Calculate totals for both genders together
        groups = [
            "private_for_profit_wage_and_salary",
            "employee_of_private_company",
            "selfemployed_in_own_incorporated_business",
            "private_not_for_profit_wage_and_salary",
            "local_government",
            "state_government",
            "federal_government",
            "selfemployed_in_own_not_incorporated_business",
            "unpaid_family_workers",
        ]
        for g in groups:
            df[f'total_{g}'] = df[f'male_{g}'] + df[f'female_{g}']

        # Calculate custom group sets
        groupsets = collections.OrderedDict({
            "government": [
                'local_government',
                'state_government',
                'federal_government',
            ],
        })
        for groupset, group_list in groupsets.items():
            df[f'total_{groupset}'] = df[[f'total_{f}' for f in group_list]].sum(axis=1)
            df[f'male_{groupset}'] = df[[f'male_{f}' for f in group_list]].sum(axis=1)
            df[f'female_{groupset}'] = df[[f'female_{f}' for f in group_list]].sum(axis=1)

        # Pass it back
        return df
