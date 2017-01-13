import shutil

old_module_dir = '/home/marco/dev/QGIS/plugins/veriso/modules/veriso_dm01'

# end config

import simplejson as json
import yaml
import os


checks_dir = os.path.join(old_module_dir, 'checks')
checks_file = os.path.join(checks_dir, 'checks.json')

with open(checks_file, 'r') as f:
    checks_file = json.load(f)


def write_yaml(file_path, content):
    with open(file_path, 'w+') as f:
        f.write('---\n')
        yaml.dump(content, f, default_flow_style=False)


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


for topic in checks_file['checks']:
    topic_name = topic['file']
    topic_file_path = os.path.join(checks_dir, topic_name + '.json')
    dir_name = topic_name[6:]
    dest_dir_path = os.path.join(checks_dir, dir_name)

    # create topics dir
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    # write topic file
    yaml_topic_file_path = os.path.join(dest_dir_path, 'topic.yml')
    del topic['file']
    write_yaml(yaml_topic_file_path, topic)

    # read topic_xxxxx.json
    checks_file = load_json(topic_file_path)
    last_file_name = None
    for check in checks_file['checks']:
        try:
            subdir, file_name = check['file'].split('.')
            orig = os.path.join(old_module_dir, subdir, file_name + '.py')
            dest = os.path.join(dest_dir_path, file_name)
            shutil.copyfile(orig, dest + '.py')
            del check['id']
            del check['file']
            write_yaml(dest + '.yml', check)
            last_file_name = file_name
        except KeyError:
            if check['name'] == 'separator':
                dest = os.path.join(
                        dest_dir_path, last_file_name + '_separator')
                open(dest, 'a').close()
