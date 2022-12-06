import os
from os.path import dirname, join
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers import index
#import index
import pymongo


def test_github_action():
   
    assert 1==1