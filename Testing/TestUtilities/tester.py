# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry
#
# Test utility for FW/SDEC integration tests.
#
# Very regression prone -- use caution!

import os

INTERMEDIATE_RESULTS_DIR = "intermediate_results"

class Tester:
    def __init__(self):
        self.__results = []

    def assert_result(self, predicate: bool, msg: str):
        if predicate:
            self.__results.append( (1, msg) )
        else:
            self.__results.append( (0, msg) )

    # Should write out results in the firmware intermediate
    # style AND sdec's internal test result style if it
    # ever gets made.
    def write_results(self, test_dir: str, results_name: str):
        # get results file
        if len(self.__results) == 0:
            return # do nothing
        # construct path
        file_name = os.path.join(test_dir, INTERMEDIATE_RESULTS_DIR, results_name)
        with open(file_name, "w") as f:
            for line in self.__results:
                f.write(str(line[0]) + line[1] + "\n")