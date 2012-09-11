# -*- coding: utf-8 -*-
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from setuptools import setup, find_packages

from torneira import __version__

README_FILE = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='torneira',
    version=__version__,
    description="Torneira is a lightweight web framework build on top of Tornado",
    long_description=open(README_FILE).read(),
    keywords=['torneira', 'tornado'],
    author='Marcel Nicolay',
    author_email='marcel.nicolay@gmail.com',
    url='http://github.com/marcelnicolay/torneira',
    license='OSI',
    packages=find_packages(),
    package_dir={"torneira": "torneira"},
    include_package_data=True,
    install_requires=[
        "tornado>=2.3",
        "python-daemon>=1.6",
    ],
    entry_points={
        'console_scripts': [
            'torneira = torneira.runner:run',
        ],
    },
    test_suite="nose.collector",
    tests_require=[
        "nose>=1.1.2",
        "fudge>=1.0.3",
        "coverage>=3.5.1",
    ],
)
