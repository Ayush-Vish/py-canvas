import json
import sys

DEFAULT_JSON = False
DEFAULT_TABLE = False
DEFAULT_SKIP_HEADERS = False

# keys: [(items key, title, pretty title), ...]
def cli_list(items, keys, table = DEFAULT_TABLE, skip_headers = DEFAULT_SKIP_HEADERS,
        collective_name = 'items', sort_key = 'id', output_json = DEFAULT_JSON):
    items = list(sorted(items, key = lambda item: item.get(sort_key, '')))

    if (output_json):
        _cli_list_json(items = items, keys = keys)
    elif (table):
        _cli_list_table(items = items, keys = keys, skip_headers = skip_headers, collective_name = collective_name)
    else:
        _cli_list_plain(items = items, keys = keys, collective_name = collective_name)

    return 0

def _cli_list_json(items, keys):
    json_data = []

    for item in items:
        values = {}

        for items_key, title, _  in keys:
            value = item.get(items_key)
            values[title] = value

        json_data.append(values)

    print(json.dumps(json_data, indent = 4, sort_keys = True))

def _cli_list_table(items, keys, skip_headers, collective_name):
    if (len(items) == 0):
        print("No %s found." % (collective_name), file = sys.stderr)
        return 0

    if (not skip_headers):
        print("\t".join([key_set[1] for key_set in keys]))

    for item in items:
        values = {}

        for items_key, _, _ in keys:
            value = item[items_key]
            if (value is None):
                value = ''

            values[items_key] = str(value).strip()

        print("\t".join(map(_clean_cell, [values[key_set[0]] for key_set in keys])))

def _cli_list_plain(items, keys, collective_name):
    if (len(items) == 0):
        print("No %s found." % (collective_name), file = sys.stderr)
        return 0

    for i in range(len(items)):
        item = items[i]

        values = {}
        for items_key, _, _ in keys:
            value = item[items_key]
            if (value is None):
                value = ''

            values[items_key] = str(value).strip()

        if (i != 0):
            print()

        for key_set in keys:
            print("%s: %s" % (key_set[2], values[key_set[0]]))

def _clean_cell(text):
    """
    Clean the text that will be in a TSV cell.
    """

    return str(text).replace("\t", " ").replace("\n", " ")

def add_output_args(parser):
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-t', '--table', dest = 'table',
        action = 'store_true', default = DEFAULT_TABLE,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')

    group.add_argument('--json', dest = 'output_json',
        action = 'store_true', default = DEFAULT_JSON,
        help = 'Output in JSON format instead of TSV')

    group.add_argument('--skip-headers', dest = 'skip_headers',
        action = 'store_true', default = DEFAULT_SKIP_HEADERS,
        help = 'Skip headers when outputting as a table (default: %(default)s).')
