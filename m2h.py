import sys, subprocess, os.path, time

# alias m2h="python ~\Desktop\30DaysOfBlogging\m2h.py" 
# Run the script with `m2h <markdown file>`

# One argument, which is the name of the to be created markdown file
if len(sys.argv) is not 2:
    print("ERROR: One and only one argument needed. Markdown file")
    sys.exit()

md_file = sys.argv[1]

# If file doesnot exist, just exit
if not os.path.exists(md_file):
    print("ERROR: Markdown file '" + md_file + "' does not exist. Exiting")
    sys.exit()

# hello.md -> hello.html
html_file = md_file[:-2] + "html"

# Run pandoc on the markdown file every 10 seconds
while True:
    # -f markdown-smart will make sure that it won't convert single quotes to curly single quotes
    subprocess.run(['pandoc.exe', '-f', 'markdown-smart', md_file, '-o', html_file])
    time.sleep(5)
