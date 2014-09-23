"""A Python movescount parser"""
from HTMLParser import HTMLParser, HTMLParseError
import urllib, re, sys

class MoveParser(HTMLParser):
    """Parses moves and move details from movescount."""
    URL_PREFIX = "http://www.movescount.com/members/"

    def __init__(self):
        """init."""
        HTMLParser.__init__(self)
        # Used for deciding when to read data.
        self.in_move = False
        # Store move details.
        self.move_titles = []
        self.move_dates = []
        self.move_durations = []
        # Store all move data. Created after parsing.
        self.move_data = None

    def _read_page_data(self, url_suffix):
        """Reads webpage data."""
        try:
            data = urllib.urlopen(self.URL_PREFIX+url_suffix).read()
        except IOError:
            raise
        return data

    def _format_data(self):
        """Format data."""
        self.move_data = zip(self.move_titles, \
            self.move_dates, self.move_durations)

    def _test_content_class(self, name, value, regex):
        """Test content in class."""
        try:
            if name == "class" and re.match(regex, value).group(0):
                return True
        except AttributeError:
            pass

    def _test_content_href(self, name, value, regex):
        """Test content in href."""
        try:
            if name == "href" and re.match(regex, value).group(0):
                return True
        except AttributeError:
            pass
        return False

    def _test_title(self, name, value):
        """Get move title."""
        return self._test_content_class(name, value, r"icon-\d{2} box")

    def _test_date(self, name, value):
        """Test move date."""
        return self._test_content_class(name, value, r"span2 first-item")

    def _test_duration(self, name, value):
        """Test move duration."""
        return self._test_content_href(name, value, r"/moves/move\d+")

    def _handle_title_data(self, data):
        """Handle title data."""
        self.move_titles.append(data)

    def _handle_date_data(self, data):
        """Handles date data."""
        self.move_dates.append(data)

    def _handle_duration_data(self, data):
        """Handles duration data."""
        self.move_durations.append(data)

    def handle_starttag(self, tag, attrs):
        """Handle start tag."""
        # Set to false every tag to avoid reading other data.
        self.in_move = False
        for name, value in attrs:
            if self._test_title(name, value):
                try:
                    self._handle_title_data(attrs[1][1])
                except:
                    raise
                continue
            if self._test_date(name, value):
                # Start reading data.
                self.in_move = True
                continue
            if self._test_duration(name, value):
                # Start reading data.
                self.in_move = True
                continue

    def handle_endtag(self, tag):
        """Handle end tag."""
        if tag == "html":
            # Finish up.
            self._format_data()

    def handle_data(self, data):
        """Handles data when in_move is True."""
        if self.in_move:
            data = data.strip()
            try:
                if re.match(r"\d+.\d+.\d{4}", data).group(0):
                    self._handle_date_data(data)
            except AttributeError:
                pass
            try:
                if re.match(r"\d+:\d+", data).group(0):
                    self._handle_duration_data(data)
            except AttributeError:
                pass
            return

    def get_latest_moves(self, username):
        """Get latest moves from user."""
        data = self._read_page_data(username)
        try:
            self.feed(data)
        except HTMLParseError:
            raise
        return self.move_data

    def get_move_details(self, move_id):
        """Get move details."""
        return "Not yet implemented"


if __name__ == '__main__':
    # Run with: "python pymoves.py USERNAME".
    mv = MoveParser()
    if len(sys.argv) > 1:
        username = sys.argv[1].lower()
        moves = mv.get_latest_moves(username)
        print "Latest moves for " + username + ":"
        for x, y, z in moves:
            print x, '\t\t', y, '\t\t', z
    else:
        print "Run with \"python pymoves.py USERNAME\""
