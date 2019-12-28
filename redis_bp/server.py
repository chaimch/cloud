from resource.docker import DockerResource


class RedisInstanceServer(DockerResource):
    def post(self):
        """创建redis实例"""
        image_name = 'redis'
        name = 'test'

        container = self.get_or_create_container(image_name,
                                                 name=name,
                                                 ports={'6379/tcp': 6379})
        return self.container_to_json(container)


class RedisConfigServer(DockerResource):
    def get(self):
        """获取redis配置"""
        name = 'test'

        container = self.get_container(name)

        return self.container_to_json(container)
