# Should read in Article title, tags from the md file
# Call the modifications file and do it on the output html
# Publish to Blogger but as a draft

import sys, os, re
import blogger_publish, medium_publish
import CommentParser


def main():
    # One argument, which is the name of the to be created markdown file
    if len(sys.argv) is not 2:
        print("ERROR: One and only one argument needed. Article to publish")
        sys.exit()

    html_file = sys.argv[1]

    # Handle user's mistake by taking care of file extensions for him
    # If md file was given when html was intended
    if html_file.endswith(".md"):
        html_file = html_file[:-2] + "html"
    elif not html_file.endswith(".html"):
        html_file = html_file + ".html"

    if not os.path.exists(html_file):
        print('File', html_file, 'does not exist. Exiting.')
        sys.exit()

    with open(html_file) as file:
        html_file_contents = file.read()

    re_comments = re.compile('\s*<!--(.*)-->', re.DOTALL)
    comments_text = re_comments.search(html_file_contents).group(1).strip()
    comments_parser = CommentParser.parse_comments(comments_text)

    if comments_parser.destination.lower() == 'blogger':
        blogger_publish.publish(html_file, comments_parser.title, comments_parser.labels, comments_parser.post_id)
    elif comments_parser.destination.lower() == 'medium':
        medium_publish.publish(html_file, comments_parser.title, comments_parser.labels, comments_parser.post_id)
    else:
        print(
            'Unknown destination: ' + comments_parser.destination + '. Supported destinations are Blogger and Medium.')


if __name__ == '__main__':
    main()
