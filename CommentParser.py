import re


# Read the comments tags from the html file
class CommentParser:
    def __init__(self, title, labels, post_id, destination):
        self.title = title
        self.labels = labels
        self.post_id = post_id
        self.destination = destination


# Parse a comments string into a CommentParser object
def parse_comments(full_string):
    re_title = re.compile('\s*title\s*:(.*)', re.IGNORECASE)
    re_labels = re.compile('\s*labels\s*:(.*)', re.IGNORECASE)
    re_post_id = re.compile('\s*postid\s*:(.*)', re.IGNORECASE)
    re_destination = re.compile('\s*destination\s*:(.*)', re.IGNORECASE)

    title = re_title.search(full_string).group(1).strip()
    labels_text = re_labels.search(full_string).group(1).strip()

    labels = [l.strip() for l in labels_text.split(",")] if labels_text else []
    post_id = re_post_id.search(full_string).group(1).strip()
    destination = re_destination.search(full_string).group(1).strip()

    # print(f"'{title}', '{labels}', '{post_id}', '{destination}'", flush=True)

    return CommentParser(title, labels, post_id, destination)
