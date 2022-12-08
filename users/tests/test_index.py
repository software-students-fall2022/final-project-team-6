import os
from os.path import dirname, join, abspath
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from controllers import index
#import index
import pymongo


def test_github_action():
   
    assert 1==1