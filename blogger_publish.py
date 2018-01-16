# Call easyblogger
# Client secret and authentication is already stored in ~/.easyblogger.credentials
# blogid is stored in ~/.easyblogger

import subprocess
import blogger_modifications


def publish(html_file, title, labels, post_id):
    # print('publishing', html_file, 'with title', title, 'labels', labels, 'and post-id', post_id, flush=True)
    print(post_id)
    # Modify html as needed.
    blogger_modifications.modify(html_file)

    # If post-id doesnt already exist,
    if not post_id:
        command = f'easyblogger.exe post -t "{title}" -l "{", ".join(labels)}" -f "{html_file}"'
    else:
        command = f'easyblogger.exe update -t "{title}" -l "{", ".join(labels)}" -f "{html_file}" --publish {post_id}'
    subprocess.run(command)
