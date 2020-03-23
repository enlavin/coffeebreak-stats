import feedparser
from .episode import Episode
import pandas as pd

IVOOX_FEED_URL = 'https://www.ivoox.com/podcast-coffee-break-senal-ruido_fg_f1172891_filtro_1.xml'


def to_df(episodes, wants_guest_columns=False):
    columns = [
        'id',
        'title',
        'number',
        'duration',
        'length',
        'guests',
        'summary',
    ]

    if wants_guest_columns:
        guests = set([name for ep in episodes for name in ep.guests])

    objs = []
    for ep in episodes:
        row = {}
        for col in columns:
            row[col] = getattr(ep, col)

        row['guests_count'] = len(getattr(ep, 'guests'))

        if wants_guest_columns:
            for guest in guests:
                row[guest] = int(guest in ep.guests)

        objs.append(row)

    df = pd.DataFrame(data=objs)
    return df


def load_episodes(feed_url=None):
    if (feed_url is None):
        feed_url = IVOOX_FEED_URL
    
    feed = feedparser.parse(feed_url)
    return [Episode(e) for e in feed['entries']]


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("guests_csv.py <feed url> <output csv>")
        sys.exit(1)

    feed_url = sys.argv[1]
    episodes = load_episodes(feed_url)
    print('\n'.join([ep.id + ': ' + ', '.join(ep.guests) for ep in episodes]))

    df = to_df(episodes, wants_guest_columns=True)
    df.to_csv(sys.argv[2], index=False)

    #durations = [convert_to_seconds(e['itunes_duration']) for e in feed['entries']]
    #guests = [(re.findall('(ep\s*[0-9_]+)', e['title'], re.I)[0], re.split('\s*(?:,|;)\s*', re.findall('En la foto[^A-Z]*:?\s*([^.]*)', preprocess(e['summary']), re.S)[0])) for e in feed['entries'] if e['summary'].find('En la foto') >= 0]