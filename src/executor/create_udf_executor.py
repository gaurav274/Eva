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

from src.catalog.catalog_manager import CatalogManager
from src.planner.create_udf_plan import CreateUDFPlan
from src.executor.abstract_executor import AbstractExecutor
import tempfile
import os.path


class CreateUDFExecutor(AbstractExecutor):

    def __init__(self, node: CreateUDFPlan):
        super().__init__(node)

    def validate(self):
        pass

    def exec(self):
        """Create udf executor

        Calls the catalog to create udf metadata.
        """
        if (self.node.if_not_exists):
            # check catalog if it already has this udf entry
            return
        io_list = []
        io_list.extend(self.node.inputs)
        io_list.extend(self.node.outputs)
        udf_metadata = CatalogManager().create_udf(
            self.node.name, self.node.impl_path, self.node.type, io_list)