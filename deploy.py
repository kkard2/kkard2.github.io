import os
import shutil


def process_templating(src_file, dest_dir, start_dir, template_file):
    relative_path = os.path.relpath(src_file, start_dir)
    dest_file = os.path.join(dest_dir, relative_path)

    os.makedirs(os.path.dirname(dest_file), exist_ok=True)

    file_extension = src_file.split('.')[-1]

    title = 'kkard2'

    if 'index.html' in relative_path:
        title += '/' + relative_path.split('index.html')[0].replace('\\', '/')
    else:
        title += '/' + relative_path.replace('\\', '/')

    content = ''

    if file_extension != 'html':
        shutil.copy(src_file, dest_file)
        return

    with open(src_file, 'r') as source:
        for line in source:
            if '<!-- #include' in line:
                include_file = line.split('<!-- #include')[1]
                include_file = include_file.split('-->')[0].strip()
                include_path = os.path.join(start_dir, include_file)
                with open(include_path, 'r') as include_content:
                    content += include_content.read()
            elif '<!-- #title' in line:
                title = line.split('<!-- #title')[1].split('-->')[0].strip()
            else:
                content += line

    with open(template_file, 'r') as template:
        with open(dest_file, 'w') as destination:
            for template_line in template:
                if '##content##' in template_line:
                    destination.write(content)
                elif '##title##' in template_line:
                    destination.write(
                            template_line.replace('##title##', title))
                else:
                    destination.write(template_line)


def process_autolinks(dest_file):
    file_extension = src_file.split('.')[-1]

    if file_extension != 'html':
        return

    content = ''
    tags = ['h1', 'h2', 'h3']
    closing = False

    with open(dest_file, 'r') as source:
        for line in source:
            for tag in tags:
                # only accepts headings witout styling
                if '<' + tag + '>' in line:
                    if closing:
                        print("sth no yes in " + dest_file + " line " + line)
                        return


            # if '<!-- #include' in line:
            #     include_file = line.split('<!-- #include')[1]
            #     include_file = include_file.split('-->')[0].strip()
            #     include_path = os.path.join(start_dir, include_file)
            #     with open(include_path, 'r') as include_content:
            #         content += include_content.read()
            # elif '<!-- #title' in line:
            #     title = line.split('<!-- #title')[1].split('-->')[0].strip()
            # else:
            #     content += line



start_dir = "./src"
dest_dir = "./docs"
template_file = "./template.html"

if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)

for root, dirs, files in os.walk(start_dir):
    for file in files:
        src_file = os.path.join(root, file)
        process_templating(src_file, dest_dir, start_dir, template_file)
