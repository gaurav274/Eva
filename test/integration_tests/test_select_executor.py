# coding=utf-8
# Copyright 2018-2020 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
import os
import pandas as pd
import numpy as np

from src.parser.parser import Parser
from src.optimizer.statement_to_opr_convertor import StatementToPlanConvertor
from src.optimizer.plan_generator import PlanGenerator
from src.executor.plan_executor import PlanExecutor
from src.catalog.catalog_manager import CatalogManager
from src.models.storage.batch import Batch
from test.util import create_sample_video
from test.util import create_dummy_batches

NUM_FRAMES = 10


class SelectExecutorTest(unittest.TestCase):

    def setUp(self):
        CatalogManager().reset()
        create_sample_video()

    def tearDown(self):
        os.remove('dummy.avi')

    def perform_query(self, query):
        stmt = Parser().parse(query)[0]
        l_plan = StatementToPlanConvertor().visit(stmt)
        p_plan = PlanGenerator().build(l_plan)
        return PlanExecutor(p_plan).execute_plan()

    def test_should_load_and_select_in_table(self):
        query = """LOAD DATA INFILE 'dummy.avi' INTO MyVideo;"""
        self.perform_query(query)

        select_query = "SELECT id FROM MyVideo;"
        actual_batch = self.perform_query(select_query)
        expected_rows = [{"id": i} for i in range(NUM_FRAMES)]
        expected_batch = Batch(frames=pd.DataFrame(expected_rows))
        self.assertTrue(actual_batch, expected_batch)

        select_query = "SELECT data FROM MyVideo;"
        actual_batch = self.perform_query(select_query)
        expected_rows = [{"data": np.array(np.ones((2, 2, 3))
                                           * 0.1 * float(i + 1) * 255,
                                           dtype=np.uint8)}
                         for i in range(NUM_FRAMES)]
        expected_batch = Batch(frames=pd.DataFrame(expected_rows))
        self.assertTrue(actual_batch, expected_batch)

        # select * is not supported
        select_query = "SELECT id,data FROM MyVideo;"
        actual_batch = self.perform_query(select_query)
        expected_batch = list(create_dummy_batches())[0]
        self.assertTrue(actual_batch, expected_batch)


if __name__ == "__main__":
    unittest.main()