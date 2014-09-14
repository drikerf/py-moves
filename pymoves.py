"""A Python scraper for movescount."""
from HTMLParser import HTMLParser

class MoveParser(HTMLParser):
    """Parses moves and move details from movescount."""

    def __init__(self):
        """init."""
        pass

    def handle_starttag(self, tag, attrs):
        """Handle start tag."""
        pass

    def handle_endtag(self, tag):
        """Handle end tag."""
        pass

    def handle_data(self, tag):
        """Handles data."""
        pass

    def get_latest_moves(self, username):
        """Get latest moves from user."""
        pass

    def get_move_details(self, move_id):
        """Get move details."""
        pass


if __name__ == '__main__':
    print "Oh..."
