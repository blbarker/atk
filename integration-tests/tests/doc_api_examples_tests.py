#
# Copyright (c) 2015 Intel Corporation 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest


import sys
sys.path.insert(0, '/home/blbarker/dev/atk/python-client')

import trustedanalytics as ta
ta.server.port = 19099
from trustedanalytics.meta.doc import parse_for_doctest, DocExamplesPreprocessor
from doc_api_examples_exemptions import exemptions

import doctest
doctest.ELLIPSIS_MARKER = DocExamplesPreprocessor.doctest_ellipsis

import sys
current_module = sys.modules[__name__]

import os
#print "examples=%s" % examples
here = os.path.dirname(os.path.abspath(__file__))
path_to_examples = os.path.join(here, "../../doc-api-examples/src/main/resources/python")
path_to_core = os.path.join(here, "../../python-client/trustedanalytics/core")
import fnmatch


__test__ = {}


def filter_exemptions(paths):
    chop = len(path_to_examples) + 1  # the + 1 is for the extra forward slash
    filtered_paths = [p for p in paths if p[chop:] not in exemptions]
    return filtered_paths


def print_list(x):
    for item in x:
        print str(item)


def get_all_example_rst_file_paths():
    paths = []
    for root, dirnames, filenames in os.walk(path_to_examples):
        for filename in fnmatch.filter(filenames, '*.rst'):
            paths.append(os.path.join(root, filename))
    return paths


def add_doctest_file(full_path):
    with open(full_path) as f:
        content = f.read()
    cleansed = parse_for_doctest(content)
    print "Adding content for %s" % full_path
    __test__[full_path] = cleansed


def init_tests(files):
    if isinstance(files, basestring):
        files = [files]
    __test__.clear()
    for f in files:
        add_doctest_file(f)


def run_tests(files=None, verbose=False):
    #print "ellipsis=%s" % doctest.ELLIPSIS_MARKER
    files = files or get_all_example_rst_file_paths()
    # if files:
    #     print "running doctest on these files:"
    #     for f in files:
    #         print f
    # else:
    #     print "No Example files found"
    init_tests(files or get_all_example_rst_file_paths())
    return doctest.testmod(m=current_module,
                    raise_on_error=False,
                    exclude_empty=True,
                    verbose=verbose,
                    report=True,
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

verbose = False  # set to True for debug

class ExampleDocTests(unittest.TestCase):

    def test_rst_examples(self):
        files = get_all_example_rst_file_paths()
        filtered_files = filter_exemptions(files)
        results = run_tests(filtered_files, verbose=verbose)
        self.assertEqual(0, results.failed, "Tests in the example documentation failed.")

    def test_clientside_examples(self):
        files = [os.path.join(path_to_core, "frame.py")]
        results = run_tests(files, verbose=verbose)
        self.assertEqual(0, results.failed, "Tests in the clientside example documentation failed.")

if __name__ == "__main__":
    unittest.main()
