from setuptools import setup

setup(
    name="tester",
    options = {
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                './Data/*',
                '**/*.bam',
                '**/*.ursinamesh'
            ],
            'gui_apps': {
                'Your Program Name': 'main.py',
            },
            'plugins': [
                'pandagl',
                'p3openal_audio'
            ],
            'platforms':['win_amd64'],
            'log_filename': './output.log',
            'log_append': False,
        }
    }
)