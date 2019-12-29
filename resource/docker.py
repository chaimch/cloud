import logging

import docker
from docker.errors import NotFound

from const.enum import ContainerStatus
from resource.base import BaseResource


class DockerResource(BaseResource):
    def __init__(self):
        self.dc = self.docker_client = docker.from_env()
        self.logger = self._get_default_logger()

    @classmethod
    def _get_default_logger(cls):
        """获取默认的logger"""
        logging.basicConfig(format='%(asctime)s.%(msecs)d  %(module)s:%(process)s  %(levelname)s  %(message)s',
                            level=logging.INFO)
        logger = logging.getLogger('DockerResource')
        return logger

    def get_container(self, name=None, id=None):
        """获取指定容器"""
        try:
            container = self.dc.containers.get(name or id)
        except NotFound as e:
            self.logger.info(e)
            container = None
        return container

    def create_container(self, image_name, name=None, record_logging=False, **kwargs):
        """创建容器"""
        container = self.dc.containers.run(image_name,
                                           name=name,
                                           detach=True,
                                           **kwargs)
        # 记录容器执行日志
        if record_logging:
            self.log_container(container)
        return container

    def get_or_create_container(self, image_name, name=None, id=None, record_logging=False, **kwargs):
        """获取或创建容器"""

        # 获取容器
        container = self.get_container(name or id)
        created = False

        # 不存在则创建容器
        if not container:
            container = self.create_container(image_name,
                                              name=name,
                                              record_logging=record_logging,
                                              **kwargs)
            created = True

        return created, container

    def remove_container(self, container):
        """移除容器"""
        if container.status == ContainerStatus.running.name:
            raise ValueError('容器正在运行, 不允许删除')

        res = container.remove()
        self.logger.info(f'{container.name} has been remove, res: {res}')
        return res

    def container_to_json(self, container, detail=False, **kwargs):
        """容器对象序列化为json"""
        resp = {}
        if not container:
            return resp

        image_attrs = container.image.attrs
        resp = dict(kwargs,
                    id=container.id,
                    short_id=container.short_id,
                    repotags=image_attrs['RepoTags'],
                    labels=container.labels,
                    name=container.name,
                    ports=container.ports,
                    status=container.status,
                    create_time=image_attrs['Created'],
                    )

        if detail:
            attrs = container.attrs
            host_config = attrs['HostConfig']
            resp['total_memory'] = host_config['Memory']
        return resp

    def log_container(self, container):
        """打印容器执行日志"""
        logs = container.logs()
        self.logger.info(logs)
