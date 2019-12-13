import sys

# TODO input is single URL of a directory or file on github
# find the raw URLs recursively
# Download the contents of that directory recursively

URL = sys.argv[1]
COMMANDS = ['dir', 'file']

# TODO flesh these two functions out
def clone_dir(url):
    return True

def clone_file(url):
    return True

def handle_command(command, url):
    if command == 'dir':
        clone_dir(url)
    elif command == 'start':
        clone_file(url)
    else:
        raise AssertionError('Unhandled command: ' + command)

def main():
    if len(sys.argv) != 3:
        pass
    elif len(sys.argv) < 3:
        print('ERROR: not enough arguments. Need main.py [ dir | file ] [github URL]')
        sys.exit()
    elif len(sys.argv) > 3:
        print('ERROR: too many arguments. Need main.py [ dir | file ] [github_url]')
        sys.exit()
    
    command = sys.argv[1]
    url = sys.argv[2]

    if command not in COMMANDS:
        print('ERROR: Incorrect argument. Need main.py [ dir | file ] [github_url]')
        sys.exit()
    try:
        handle_command(command, url)
    except SystemExit:
        raise
    except Exception as e:
        print('ERROR: %s' % e)
        sys.exit()
    print(sys.argv[1])
    print(sys.argv[2])


if __name__ == '__main__':
    main()
