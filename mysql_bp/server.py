from mysql_bp.form import MysqlInstanceForm, MysqlConfigForm
from resource.docker import DockerResource
from resource.os import OSResource


class MysqlInstanceServer(DockerResource, OSResource):
    def check_params(self, *args, **kwargs):
        return MysqlInstanceForm(
            data=dict(
                self.params,
                resource=self)
        ).check_for_return()

    def post(self):
        """创建mysql实例"""
        image_name = self.params['image_name']
        name = self.params['name']
        ports = self.params['ports']
        mem_limit = self.params['mem_limit']
        database = self.params['database']
        charset = self.params['charset']

        password = self.generate_password()

        _, container = self.get_or_create_container(image_name,
                                                    command=[f'--character-set-server={charset}',
                                                             f'--collation-server={charset}_unicode_ci'],
                                                    name=name,
                                                    ports=ports,
                                                    mem_limit=mem_limit,
                                                    environment={'MYSQL_ROOT_PASSWORD': password,
                                                                 'MYSQL_DATABASE': database})

        return self.container_to_json(container, password=password)


class MysqlConfigServer(DockerResource):
    def check_params(self, *args, **kwargs):
        return MysqlConfigForm(
            data=dict(
                self.params,
                resource=self)
        ).check_for_return()

    def get(self):
        """获取mysql配置"""
        name = self.params['name']

        container = self.get_container(name)

        return self.container_to_json(container, detail=True)
