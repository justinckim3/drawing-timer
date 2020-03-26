import json

settings_json = json.dumps([
    {
        'type': 'path',
        'title': 'Images Folder',
        'desc': 'Select the directory folder that contain the images to use',
        'section': 'session',
        'key': 'dirpath'
    },
    {
        'type': 'options',
        'title': 'Pose Length',
        'desc': 'Choose how long each pose will be.',
        'section': 'session',
        'key': 'poselength',
        'options': ['30 seconds', '1 Minute', '3 Minutes', '5 Minutes', '10 Minutes', '15 Minutes', '25 Minutes']
    },
    {
        'type': 'bool',
        'title': 'Set pose limit',
        'desc': 'Turn on to limit how many images you want the program to display',
        'section': 'session',
        'key': 'limittoggle'
    },
    {
        'type': 'numeric',
        'title': 'Number of Poses',
        'desc': 'Enter amount of poses for the set',
        'section': 'session',
        'key': 'totalposes'
    },
    {
        'type': 'bool',
        'title': 'Shuffle Images',
        'desc': 'Shuffle order of images. If turned off, order will in order of file name. Images reset after every app launch.',
        'section': 'session',
        'key': 'randomtoggle'
    },
    {
        'type': 'bool',
        'title': 'Loop Images',
        'desc': 'Loop through directory after last image. If turned off, when the last image is reached, timer will stop and session will end.',
        'section': 'session',
        'key': 'looptoggle'
    }, 
    {
        'type': 'bool',
        'title': 'Play Sounds',
        'desc': 'Play alert sound before end of each pose',
        'section': 'session',
        'key': 'soundtoggle'
    }
])
