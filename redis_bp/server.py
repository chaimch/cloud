from redis_bp.form import RedisConfigForm, RedisInstanceForm
from resource.docker import DockerResource
from resource.os import OSResource


class RedisInstanceServer(DockerResource, OSResource):
    def check_params(self, *args, **kwargs):
        return RedisInstanceForm(
            data=dict(
                self.params,
                resource=self)
        ).check_for_return()

    def post(self):
        """创建redis实例"""
        image_name = self.params['image_name']
        name = self.params['name']
        ports = self.params['ports']
        mem_limit = self.params['mem_limit']
        password = self.generate_password()

        _, container = self.get_or_create_container(image_name,
                                                    command=[f'--requirepass {password}'],
                                                    name=name,
                                                    ports=ports,
                                                    mem_limit=mem_limit)

        return self.container_to_json(container, password=password)


class RedisConfigServer(DockerResource):
    def check_params(self, *args, **kwargs):
        return RedisConfigForm(
            data=dict(
                self.params,
                resource=self)
        ).check_for_return()

    def get(self):
        """获取redis配置"""
        name = self.params['name']

        container = self.get_container(name)

        return self.container_to_json(container, detail=True)
