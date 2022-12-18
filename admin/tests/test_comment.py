import sys
from os.path import dirname, join, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from controllers.comment import Comment

class Tests:
    def test_comment(self):
        c = Comment("a", "b", 4, "c")
        assert c.username == "a"
        assert c.comment == "b"
        assert c.rating == 4
        assert c.comment_id == "c"