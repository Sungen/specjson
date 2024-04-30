# specjson
simple python script to convert specjson to podspec

# convert podspec to podspec.json
pod ipc spec MyLibrary.podspec > MyLibrary.podspec.json

# convert podspec.json to podspec
python3 spec-json.py --input MyLibrary.podspec.json --output MyLibrary.podspec

