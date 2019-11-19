import re
from abc import ABC

from flaskps.serverside_dt.serverside_table import ServerSideTable


class DocentesServerSideTable(ServerSideTable, ABC):
    """
    Retrieves the values specified by Datatables in the request and processes
    the data that will be displayed in the table (filtering, sorting and
    selecting a subset of it).
    Attributes:
        request: Values specified by DataTables in the request.
        data: Data to be displayed in the table.
        column_list: Schema of the table that will be built. It contains
                     the name of each column (both in the data and in the
                     table), the default values (if available) and the
                     order in the HTML.
    """

    def _custom_filter(self, data):
        """
        Args:
            data: Data to be displayed by DataTables.
        Returns:
            Filtered data.
        """

        def check_row_firstname(row):
            """ Checks whether a row should be displayed or not. """
            value = row[self.columns[2]["column_name"]]
            regex = "(?i)" + self.request_values["sSearch_2"]
            if re.compile(regex).search(str(value)):
                return True
            return False

        def check_row_lastname(row):
            """ Checks whether a row should be displayed or not. """
            value = row[self.columns[3]["column_name"]]
            regex = "(?i)" + self.request_values["sSearch_3"]
            if re.compile(regex).search(str(value)):
                return True
            return False

        rows_f1 = [row for row in data if check_row_firstname(row)]
        return [row for row in rows_f1 if check_row_lastname(row)]
