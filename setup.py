from setuptools import setup, find_namespace_packages

setup(
    name="Baker",
      version="1.0.0",

    author="Pratap",

    description="Professional Ubuntu Cache Cleaning Utility",

    packages=find_namespace_packages(
        exclude=[
            "tests",
            "tests.*",
            "Guardian.tests",
            "Guardian.tests.*",
        ]
    ),

    include_package_data=True,

    install_requires=[

        "rich",

        "textual",

        "plotext",
        "psutil"

    ],

    entry_points={

        "console_scripts":[

            "cacheclean=cli.cacheclean:main"

        ]

    }
)