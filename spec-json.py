import json
import argparse

def get_all_keys(json_obj, keys=None):
    if keys is None:
        keys = []
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            keys.append(k)
            if isinstance(v, (dict, list)):
                get_all_keys(v, keys)
    elif isinstance(json_obj, list):
        for item in json_obj:
            get_all_keys(item, keys)
    return keys

parser = argparse.ArgumentParser(description="json to spec")
parser.add_argument("--input", help="podspec.json")
parser.add_argument("--output", help="podspec")

args = parser.parse_args()

with open(args.input, 'r', encoding='utf-8') as file:
    data = json.load(file)

first = 'Pod::Spec.new do |s|\n'

name = '\t' + 's.name\t= ' + '\'' + data.get('name') + '\'' + '\n'
version = '\t' + 's.version\t= ' + '\'' + data.get('version') + '\'' + '\n'
summary = '\t' + 's.summary\t= ' + '\'' + data.get('summary') + '\'' + '\n'
description = '\t' + 's.description\t= ' + '\'' + data.get('description') + '\'' + '\n'

homepage = '\t' + 's.homepage\t= ' + '\'' + 'https://github.com/Sungen/specjson' + '\'' + '\n'
license = '\t' + 's.license\t= ' + '{ :type => \'MIT\', :file => \'LICENSE\' }' + '\n'
author = '\t' + 's.author\t= ' + '{ \'Sungen\' => \'jokerwu.sunny@qq.com\' }' + '\n'
source = '\t' + 's.source\t= ' + '{ :git => \'https://github.com/Sungen/specjson.git\', :tag => \"#{s.version}\" }' + '\n'
  
deployment_target = '\t' + 's.ios.deployment_target\t= ' + '\'' + '11.0' + '\'' + '\n'
requires_arc = '\t' + 's.requires_arc\t= ' + '\'' + 'true' + '\'' + '\n'

resources = data.get('resources')
if resources is None:
    resource = '#\t' + 's.resources\t= ' + '\'' + 'None' + '\'' + '\n'
elif isinstance(resources, str):
    resource = '\t' + 's.resources\t= ' + '\'' + resources + '\'' + '\n'
else:
    resources = [f"'{s}'" for s in resources]
    resource = '\t' + 's.resources\t= ' + '[' + ','.join(resources) + ']' + '\n'

frameworks = data.get('frameworks')
if frameworks is None:
    framework = '#\t' + 's.frameworks\t= ' + '\'' + 'None' + '\'' + '\n'
elif isinstance(frameworks, str):
    framework = '\t' + 's.frameworks\t= ' + '\'' + frameworks + '\'' + '\n'
else:
    frameworks = [f"'{s}'" for s in frameworks]
    framework = '\t' + 's.frameworks\t= ' + ','.join(frameworks) + '\n'

libraries = data.get('libraries')
if libraries is None:
    library = '#\t' + 's.libraries\t= ' + '\'' + 'None' + '\'' + '\n'
elif isinstance(libraries, str):
    library = '\t' + 's.libraries\t= ' + '\'' + libraries + '\'' + '\n'
else:
    libraries = [f"'{s}'" for s in libraries]
    library = '\t' + 's.libraries\t= ' + ','.join(libraries) + '\n'

vendored_frameworks = data.get('vendored_frameworks')
if vendored_frameworks is None:
    vendored_framework = '#\t' + 's.vendored_framework\t= ' + '\'' + 'None' + '\'' + '\n'
elif isinstance(vendored_frameworks, str):
    vendored_framework = '\t' + 's.vendored_framework\t= ' + '\'' + vendored_frameworks + '\'' + '\n'
else:
    vendored_frameworks = [f"'{s}'" for s in vendored_frameworks]
    vendored_framework = '\t' + 's.vendored_frameworks\t= ' + ','.join(vendored_frameworks) + '\n'

vendored_libraries = data.get('vendored_libraries')
if vendored_libraries is None:
    vendored_library = '#\t' + 's.vendored_library\t= ' + '\'' + 'None' + '\'' + '\n'
elif isinstance(vendored_libraries, str):
    vendored_library = '\t' + 's.vendored_library\t= ' + '\'' + vendored_libraries + '\'' + '\n'
else:
    vendored_libraries = [f"'{s}'" for s in vendored_libraries]
    vendored_library = '\t' + 's.vendored_libraries\t= ' + ','.join(vendored_libraries) + '\n'

dependencies = data.get('dependencies')
if dependencies is None:
    dependency = '#\t' + 's.dependency\t ' + '\'' + 'None' + '\'' + '\n'
elif isinstance(dependencies, str):
    dependency = '\t' + 's.dependency\t ' + '\'' + dependencies + '\'' + '\n'
else:
    index = 0
    dependencies = get_all_keys(dependencies)
    dependency = ''
    while index < len(dependencies):
        dependency += '\t' + 's.dependency\t ' + '\'' + dependencies[index] + '\'' + '\n'
        index += 1

end = 'end'

lines_to_write = [first, name, version, summary, description, homepage, license, author, source, deployment_target, requires_arc, library, framework, resource, vendored_framework, vendored_library, dependency, end]

with open(args.output, "w", encoding="utf-8") as file:
    for line in lines_to_write:
        file.write(line)
