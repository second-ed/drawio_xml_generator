Most of this is ripped off from `https://github.com/amrelhusseiny/drawio_network_plot/tree/main` 
but converted to attrs and simplified in places.

To use, create a node list and link list using the `NetworkNode` and `NetworkLink` objects 

```python
@attr.define
class NetworkNode:
    name: str = attr.ib(validator=[instance_of(str)])
    ip: str = attr.ib(validator=[instance_of(str)])
    node_type: str = attr.ib(validator=[instance_of(str)])


@attr.define
class NetworkLink:
    src: str = attr.ib(validator=[instance_of(str)])
    dst: str = attr.ib(validator=[instance_of(str)])
```

An example would be like this:
```python
import logging
import logging.config

from drawio_xml_generator.nodes import DrawioXMLGenerator, NetworkLink, NetworkNode
from drawio_xml_generator.config import Config

Config().set_filepath("./configs/example_config.yaml")
logging.config.fileConfig(
    "./logging.ini", defaults={"root": Config().logs_folder}
)
logger = logging.getLogger(__name__)


nodes = [
    NetworkNode("firewall_1", "", "firewall"),
    NetworkNode("router_1", "", "router"),
    NetworkNode("router_2", "", "router"),
    NetworkNode("switch_1", "", "switch"),
    NetworkNode("switch_2", "", "switch"),
    NetworkNode("switch_3", "", "switch"),
    NetworkNode("switch_4", "", "switch"),
    NetworkNode("desktop_1", "", "desktop"),
    NetworkNode("desktop_2", "", "desktop"),
    NetworkNode("desktop_3", "", "desktop"),
    NetworkNode("desktop_4", "", "desktop"),
    NetworkNode("desktop_5", "", "desktop"),
    NetworkNode("desktop_6", "", "desktop"),
    NetworkNode("desktop_7", "", "desktop"),
    NetworkNode("desktop_8", "", "desktop"),
]

links = [
    NetworkLink("firewall_1", "router_1"),
    NetworkLink("firewall_1", "router_2"),
    NetworkLink("router_1", "switch_1"),
    NetworkLink("router_1", "switch_2"),
    NetworkLink("router_2", "switch_3"),
    NetworkLink("router_2", "switch_4"),
    NetworkLink("switch_1", "desktop_1"),
    NetworkLink("switch_1", "desktop_2"),
    NetworkLink("switch_2", "desktop_3"),
    NetworkLink("switch_2", "desktop_4"),
    NetworkLink("switch_3", "desktop_5"),
    NetworkLink("switch_3", "desktop_6"),
    NetworkLink("switch_4", "desktop_7"),
    NetworkLink("switch_4", "desktop_8"),
]


xml_gen = DrawioXMLGenerator()
xml_gen.add_list_nodes(nodes)
xml_gen.add_list_links(links)
xml_gen.export()
```

Exports are saved to `outputs/` with the datetime of creation being the file name