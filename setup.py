from setuptools import setup, find_packages

setup(
    name="Baker",
      version="1.0.0",

    author="Pratap",

    description="Professional Ubuntu Cache Cleaning Utility",

    packages=find_packages(),

    include_package_data=True,

    install_requires=[

        "rich",

        "textual",

        "plotext"

    ],

    entry_points={

        "console_scripts":[

            "cacheclean=cli.cacheclean:main"

        ]

    }
)