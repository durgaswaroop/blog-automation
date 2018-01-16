import sys
import subprocess
import os.path
import inflect


# alias blog="python ~\Desktop\30DaysOfBlogging\blog.py"
# Run the script with `blog <title>`

def main():
    # One argument, which is the name of the to be created markdown file
    if len(sys.argv) is not 2:
        print("ERROR: One and only one argument needed. Title of the article")
        sys.exit()

    title = sys.argv[1]
    md_file = title + ".md"

    # If file already exists, just exit
    if os.path.exists(md_file):
        print("ERROR: Markdown file '" + md_file + "' already exists. Opening that.")
        subprocess.run(['C:/Program Files (x86)/Vim/vim80/gvim.exe', '+10', md_file])
        sys.exit()

    article_title = title.replace("_", " ").title()

    # Create the markdown file and add the title
    f = open(md_file, "w+")
    f.write(generate_comments_header(article_title))
    f.write(article_title)  # Replace underscores and title case it
    f.write("\n")
    f.write("-" * len(title))
    f.write("\n")
    f.write(generate_footer_text())
    f.close()

    # Now, create the html file
    html_file = title + ".html"
    open(html_file, "w").close()

    # Start vim with the markdown file open on line #10
    subprocess.run(['C:/Program Files (x86)/Vim/vim80/gvim.exe', '+10', md_file])


# The comments to be put on top of the file
def generate_comments_header(title):
    comments = f'''<!--
Title : {title}
Labels:
PostId: 
Destination: Blogger
-->

'''
    return comments


# Generates the standard footer text, I'm using for my series
def generate_footer_text():
    part1 = '''


That is all for this article.

******************************
For more programming articles, checkout [Freblogg](http://freblogg.com){.bodyclass} TODO:// Insert some more here as appropriate: 
[Freblogg/Vim](http://www.freblogg.com/search/label/Vim){.bodyclass}
[Freblogg/Java](http://www.freblogg.com/search/label/Java){.bodyclass}
[Freblogg/Python](http://www.freblogg.com/search/label/Python){.bodyclass}
[Freblogg/Spark](http://www.freblogg.com/search/label/Apache%20Spark){.bodyclass}

TODO:// Keep only for automation
Some articles on automation:

[Web Scraping For Beginners with Python](https://medium.com/@durgaswaroop/web-scraping-with-python-introduction-7b3c0bbb6053){.bodyclass}

[My semi automated workflow for blogging](https://medium.com/@durgaswaroop/my-semi-automated-blogging-workflow-62cba2827986){.bodyclass}

[Publish articles to Blogger automatically](https://medium.com/@durgaswaroop/publish-articles-on-blogger-in-just-one-second-2ef45586901){.bodyclass}

[Publish articles to Medium automatically](http://www.freblogg.com/2017/12/publish-articles-to-your-medium-blog-in_83.html){.bodyclass}

******************************
'''
    part2 = get_twitter_footer()
    part3 = '''
If you are interested in contributing to any open source projects and haven't found the right project or if you were unsure on how to begin, I would like to suggest my own project, [Delorean](https://github.com/durgaswaroop/delorean){.bodyclass} which is a Distributed Version control system, built from scratch in scala. You can contribute not only in the form of code, but also with usage documentation and also by identifying any bugs in its functionality.

******
Thanks for reading. See you again in the next article.'''
    return part1 + part2 + part3


def get_twitter_footer():
    days_since_challenge_started = get_days_since_challenge_started()
    e = inflect.engine()

    # 1 -> 1st, 2 -> 2nd ...
    ordinal = e.ordinal(days_since_challenge_started)

    # 22 -> Twenty two, 18 -> Eighteen ..
    days_still_left_in_words = e.number_to_words(30 - days_since_challenge_started).capitalize().replace("-", " ")

    test = f'''This is the {ordinal} article as part of my twitter challenge [#30DaysOfBlogging](https://twitter.com/durgaswaroop/status/944503750340702208){{.bodyclass}}. {days_still_left_in_words} more articles on various topics, including but not limited to, [Java](http://www.freblogg.com/search/label/Java){{.bodyclass}}, [Git](http://www.freblogg.com/search/label/Git){{.bodyclass}}, [Vim](http://www.freblogg.com/search/label/Vim){{.bodyclass}}, [Software Development](http://www.freblogg.com/search/?q=software){{.bodyclass}}, [Python](http://www.freblogg.com/search/?q=python){{.bodyclass}}, to come.

If you are interested in this, make sure to follow me on Twitter [\@durgaswaroop](https://twitter.com/durgaswaroop){{.bodyclass}}. While you're at it, Go ahead and subscribe [here on medium](https://medium.com/@durgaswaroop/){{.bodyclass}} and my [other blog](http://freblogg.com){{.bodyclass}} as well.

************'''.strip()
    return test


def get_days_since_challenge_started():
    from datetime import date
    start = date(2017, 12, 23)
    today = date.today()
    return (today - start).days + 1  # adding 1 as the 23rd December was Day #1 and not Day #0


if __name__ == '__main__':
    main()
