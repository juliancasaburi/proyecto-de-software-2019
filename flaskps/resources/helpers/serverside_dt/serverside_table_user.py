import re
from abc import ABC

from flask import session, abort, request, jsonify

from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role
from flaskps.models import siteconfig
from flaskps.models.user import User
from flaskps.resources.helpers.serverside_dt import table_schemas
from flaskps.resources.helpers.serverside_dt.serverside_table import ServerSideTable


class UsuariosServerSideTable(ServerSideTable, ABC):
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

        def check_row_username(row):
            """ Checks whether a row should be displayed or not. """
            value = row[self.columns[5]["column_name"]]
            regex = "(?i)" + self.request_values["sSearch_6"]
            if re.compile(regex).search(str(value)):
                return True
            return False

        def check_row_active(row):
            """ Checks whether a row should be displayed or not. """
            value = row[self.columns[1]["column_name"]]
            regex = "(?i)" + self.request_values["sSearch_1"]
            if re.compile(regex).search(str(value)):
                return True
            return False

        rows_f1 = [row for row in data if check_row_username(row)]
        return [row for row in rows_f1 if check_row_active(row)]


def collect_data_serverside(req):
    columns = table_schemas.SERVERSIDE_USUARIO_TABLE_COLUMNS

    users = User.all_table()

    return UsuariosServerSideTable(req, users, columns).output_result()


def serverside_table_content():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    data = collect_data_serverside(request)
    return jsonify(data)
