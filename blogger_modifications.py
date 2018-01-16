import sys
import os
import fileinput


# alias modifications="python ~/Desktop/30DaysOfBlogging/modifications.py"
# Run the script with `modifications <markdown file>`

def modify(html_file):
    # If file doesn't exist, just exit
    if not os.path.exists(html_file):
        print("ERROR: HTML file '" + html_file + "' does not exist. Exiting")
        sys.exit()

    lines = open(html_file).readlines()
    header_removed = list(filter(lambda x: "<h2" not in x, lines))
    modified_lines = list(
        map(lambda x: x.replace('<pre><code>', '<pre class="prettyprint">')
            .replace('</code></pre>', '</pre>')
            .replace('<pre class="text"><code>', '<pre class="text">'),
            header_removed))

    with open(html_file, 'w') as file:
        file.writelines(modified_lines)

    # modified_file = full_file.replace('<pre><code>', '<pre class="prettyprint">').replace('</code></pre>', '</pre>')

    # with open(html_file, 'w') as file:
    #     file.write(modified_file)


if __name__ == '__main__':
    # One argument, which is the name of the html file
    if len(sys.argv) is not 2:
        print("ERROR: One and only one argument needed. Html file")
        sys.exit()

    html_file = sys.argv[1]
    modify(html_file)
