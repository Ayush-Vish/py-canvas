import sys

import canvas.api.user.fetch
import canvas.cli.common
import canvas.cli.user.common
import canvas.config

DEFAULT_INCLUDE_ROLE = False

def run_cli(user = None, include_role = DEFAULT_INCLUDE_ROLE, **kwargs):
    raw_users = []
    if (user is not None):
        raw_users.append(user)

    users = canvas.api.user.fetch.request(users = raw_users, include_role = include_role,
            **kwargs)

    keys = canvas.cli.user.common.OUTPUT_KEYS.copy()
    if (include_role):
        keys.append(canvas.cli.user.common.ENROLLMENT_KEY)

    return canvas.cli.common.cli_list(users, keys,
            collective_name = 'user', sort_key = 'email',
            **kwargs)

def main():
    config = canvas.config.get_config(exit_on_error = True, modify_parser = _modify_parser)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'Fetch information for a user.'

    canvas.cli.common.add_output_args(parser)

    parser.add_argument('--include-role', dest = 'include_role',
        action = 'store_true', default = DEFAULT_INCLUDE_ROLE,
        help = 'Include user\'s role in the course (default: %(default)s).')

    parser.add_argument('user',
        action = 'store', type = str,
        help = 'The query for the user to fetch information about.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
