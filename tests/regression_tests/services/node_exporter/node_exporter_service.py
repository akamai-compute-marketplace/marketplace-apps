from regression_tests.services.addon_service import AddonService


class NodeExporterService(AddonService):
    """
    Actions for the node_exporter add-on over SSH
    """

    UNIT = "node_exporter"
    PORT = 9100
