#---Airflow libraries-----#
import os
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#---JSON libraries-----#
import json

#---Elsapy libraries-----#
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor
from elsapy.elssearch import ElsSearch

#---Pandas libraries-----#
import pandas as pd


class ReadWOS(BaseOperator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def execute(self, context):
        print('Getting WOS Data')