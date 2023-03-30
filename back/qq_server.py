import json
import os

from flask import request
import requests

from config import QQ_PRITE_URL, QQ_GROUP_URL
from mybasic import app, db
from myTools import *
from tables import QQ_temp
from private import REMOTE_URL, MY_QQ_ID
