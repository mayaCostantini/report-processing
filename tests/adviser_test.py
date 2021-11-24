#!/usr/bin/env python3
# thoth-report-processing
# Copyright(C) 2020 Francesco Murdaca
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Adviser test suite."""

from tests.base_test import ReportProcessingTestCase

from thoth.report_processing.components.adviser import Adviser


class TestAdviser(ReportProcessingTestCase):
    """Test implementation of adviser results."""

    _ADVISER_FOLDER_PATH = ReportProcessingTestCase.DATA / "adviser"

    def test_get_adviser_files(self) -> None:
        """Test retrieving adviser results from local path."""
        adviser_files = Adviser.aggregate_adviser_results(repo_path=self._ADVISER_FOLDER_PATH, is_local=True)
        assert adviser_files

    def test_create_adviser_dataframe_with_results(self) -> None:
        """Test create of adviser dataframe from adviser documents."""
        adviser_files = Adviser.aggregate_adviser_results(repo_path=self._ADVISER_FOLDER_PATH, is_local=True)

        dataframes = Adviser.create_adviser_dataframes(
            adviser_files=adviser_files,
        )

        assert dataframes["justifications"].shape[0] == 212

    def test_create_adviser_dataframe_histogram(self) -> None:
        """Test create of adviser dataframe for histogram plot from adviser documents."""
        adviser_files = Adviser.aggregate_adviser_results(repo_path=self._ADVISER_FOLDER_PATH, is_local=True)

        adviser_justifications_dataframe, _ = Adviser.create_adviser_justifications_and_statistics_dataframe(
            adviser_files=adviser_files,
        )

        sorted_justifications_df = Adviser.create_adviser_results_dataframe_histogram(
            adviser_type_dataframe=adviser_justifications_dataframe,
        )

        assert sorted_justifications_df.shape[0] == 51

    def test_create_adviser_dataframe_heatmap(self) -> None:
        """Test create of adviser dataframe for heatmap plot from adviser documents."""
        adviser_files = Adviser.aggregate_adviser_results(repo_path=self._ADVISER_FOLDER_PATH, is_local=True)

        dataframes = Adviser.create_adviser_dataframes(
            adviser_files=adviser_files,
        )

        adviser_heatmap_df = Adviser.create_adviser_results_dataframe_heatmap(
            adviser_type_dataframe=dataframes["justifications"],
            number_days=1,
        )

        last_date = [column for column in adviser_heatmap_df.columns][-1]
        csv = adviser_heatmap_df[[last_date]].to_csv(header=False)

        assert csv
