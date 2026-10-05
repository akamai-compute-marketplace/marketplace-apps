from regression_tests.services.addon_service import AddonService


class MysqldExporterService(AddonService):
    """
    Actions for the mysqld_exporter add-on over SSH
    """

    UNIT = "mysqld_exporter"
    PORT = 9104
