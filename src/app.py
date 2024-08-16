from kubernetes import client, config
from kubernetes.client.rest import ApiException
import os
import init
import time
import logging

VAL_TRUE = 'true'
ANNOTATION_FLAG_EXCLUDE = 'k3s-ipv6-flusher.log-z.github.com/exclude'
ANNOTATION_INTERNAL_IP = 'k3s.io/internal-ip'
ANNOTATION_EXTERNAL_IP = 'k3s.io/external-ip'

def running():
    """运行入口
    """

    cli = init_client()
    nodes = cli.list_node()
    for node in nodes.items:
        try:
            update_ip6(node, cli)
        except ApiException as e:
            logging.error("Failed to patch Node.", exc_info=True)

def init_client():
    """初始化客户端
    """

    api_client = client.ApiClient()
    return client.CoreV1Api(api_client)

def update_ip6(node, cli):
    """更新IPv6地址
    """

    node_name = node.metadata.name
    annotations = node.metadata.annotations

    # 检查是否排除的节点
    flag_exclude = annotations.get(ANNOTATION_FLAG_EXCLUDE)
    if flag_exclude == VAL_TRUE:
        return

    # 获取内部IPv6地址
    internal_ips = annotations.get(ANNOTATION_INTERNAL_IP, '').split(',')
    internal_ip6 = next(filter(isip6, internal_ips), None)
    logging.info(f'[{node_name}] internal-ip6 : {internal_ip6}')

    if not internal_ip6:
        logging.info(f'[{node_name}] Skip it.')
        return
    
    # 获取外部IPv6地址
    external_ips = annotations.get(ANNOTATION_EXTERNAL_IP, '').split(',')
    external_ip6 = next(filter(isip6, external_ips), None)
    logging.info(f'[{node_name}] external-ip6 : {external_ip6}')

    if external_ip6 == internal_ip6:
        logging.info(f'[{node_name}] Skip it.')
        return
    
    # 更新IPv6地址
    logging.info(f'[{node_name}] {external_ip6} >> {internal_ip6}')
    if external_ip6:
        external_ips.remove(external_ip6)
    
    external_ips.append(internal_ip6)
    annotations[ANNOTATION_EXTERNAL_IP] = ','.join(filter(lambda x: x, external_ips))
    body = client.V1Node(metadata=node.metadata)
    cli.patch_node(node_name, body)

def isip6(ip: str):
    """检查是否为IPv6地址
    """

    return ':' in ip


if __name__ == '__main__':
    init.init()

    interval = os.getenv('IPV6_FLUSHER_INTERVAL', 60)
    logging.info('K3s IPv6 Flusher is running.')
    logging.info(f'CONF interval = {interval}s')

    while True:
        running()
        time.sleep(interval)
