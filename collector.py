import re
import logging
import requests
from prometheus_client.core import GaugeMetricFamily


LOGGER = logging.getLogger(__name__)


class PromTargetCollector(object):

    def __init__(self, prom_targets_endpoint=None):
        self.prom_targets_endpoint = prom_targets_endpoint

    def collect(self):
        prom_target_down_count = self.get_prom_target_down_count()
        return [self.convert_gauge_metric('prom_target_down_count', prom_target_down_count)]

    def get_prom_target_html_content(self):
        headers = {'Content-Type': 'application/json'}
        connection = requests.get(self.prom_targets_endpoint, headers=headers)
        if connection.status_code == 200:
            return connection.content
        return ''

    def get_prom_target_down_count(self):
        content = self.get_prom_target_html_content()
        matches = re.findall('\sdown', content);
        return len(matches)

    @classmethod
    def convert_gauge_metric(cls, metric_key, metric_value):
        return GaugeMetricFamily(
            name=metric_key,
            documentation='from %s' % metric_key,
            value=metric_value
        )
