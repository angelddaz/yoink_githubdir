import sys
import re
import requests

# TODO input is single URL of a directory or file on github
# find the raw URLs recursively
# Download the contents of that directory recursively

URL = sys.argv[1]
COMMANDS = ['dir', 'file']

# TODO flesh these two functions out
def clone_dir(url):
    return True


def transform_url(url):
    url = url.strip()
    # NOTE current slice and dice to get URL for raw file content
    # url: https://github.com/angelddaz/presto_template/blob/master/cross-db-template.ipynb
    # transformed_url: https://raw.githubusercontent.com/angelddaz/presto_template/master/cross-db-template.ipynb
    
    # splitting out into the tiniest pieces with regex
    url_bits = re.split('([^.a-zA-Z])', url)

    for i in range(len(url_bits)):
        # [0] 'https://'
        if(i==6):
            # handling any urls that don't start with required substring
            if(''.join(url_bits[0:8])!='https://github.com/'):
                print('ERROR: URL must start with \'https://github.com/\'')
                sys.exit()
            # append important chunk
            http = ''.join(url_bits[0:6])
            
        # [1] 'username/'
        if(i==9):
            username = ''.join(url_bits[8:10])

        # [2] 'repos name/'
        if(i==10):
            # once we find a repository name we need to collect
            # all url_bits list elements and stop at a forward slash
            j = 10
            repos_name = ''
            while(url_bits[j] != '/'):
                repos_name += url_bits[j]
                j += 1
            # now adding the forward slash after repos name 
            repos_name += url_bits[j]

            # [3] 'branch_name/'
            # needs to live after the while loop to keep that counter going
            # if we've filled out [3] repos name/
            if(repos_name is not None):
                # skip 'blob' and '/'
                j+=3 
                # grabbing branch name
                branch_name = url_bits[j]
                # grabbing forward slash
                j+=1
                branch_name += url_bits[j]
                
                # taking care of the rest of the url
                # [4] 'filename' without '/'
                j+=1
                file_name = ''
                while(j < len(url_bits)):
                    file_name += url_bits[j]
                    j += 1
                # once we're done incrementing j through url_bits
                # we can append the whole file_name
                if(j==len(url_bits)):
                    # final check and removal of a forward slash at the end of the url
                    if(url_bits[len(url_bits)-1]=='/'):
                        file_name = file_name[:-1]
    transformed_url = ''.join(http)
    transformed_url += 'raw.githubusercontent.com/'
    transformed_url += username
    transformed_url += repos_name
    transformed_url += branch_name
    transformed_url += file_name
    return transformed_url, file_name


def clone_file(url):
    transformed_url, file_name = transform_url(url)
    # download!
    myfile = requests.get(transformed_url)
    # NOTE: this download directory needs to be changed to run elsewhere
    open('/home/angel/Downloads/{file}'.format(file=file_name), 'w').write(myfile.text)
    print('transformed_url: ' + transformed_url)
    return file_name


def handle_command(command, url):
    if command == 'dir':
        clone_dir(url)
    elif command == 'file':
        file_name = clone_file(url)
    else:
        raise AssertionError('Unhandled command: ' + command)
    return file_name

def main():
    if len(sys.argv) != 3:
        pass
    elif len(sys.argv) < 3:
        print('ERROR: not enough arguments. Need launcher.py [ dir | file ] [github URL]')
        sys.exit()
    elif len(sys.argv) > 3:
        print('ERROR: too many arguments. Need launcher.py [ dir | file ] [github_url]')
        sys.exit()
    
    command = sys.argv[1]
    url = sys.argv[2]

    if command not in COMMANDS:
        print('ERROR: Incorrect argument. Need launcher.py [ dir | file ] [github_url]')
        sys.exit()
    # handle_command(command, url)
    try:
        file_name = handle_command(command, url)
        print('Your file, {filename}, has successfully download.'.format(filename=file_name))
    except Exception:
        print('UNKNOWN ERROR')
        sys.exit()

if __name__ == '__main__':
    main()
