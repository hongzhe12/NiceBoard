import requests

from utils.config_set import config_instance


class GiteeGistAPI:
    def __init__(self, access_token):
        self.base_url = "https://gitee.com/api/v5/gists"
        self.access_token = access_token
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }

    def get_gists(self, page=1, per_page=20):
        """
        获取代码片段列表
        :param page: 页码
        :param per_page: 每页数量
        :return: 响应结果
        """
        params = {
            "access_token": self.access_token,
            "page": page,
            "per_page": per_page
        }
        response = requests.get(
            self.base_url,
            headers=self.headers,
            params=params
        )
        return response.json()

    def create_gist(self, files, description):
        """
        创建代码片段
        :param files: 文件字典，格式如 {"file1.txt": {"content": "文件内容"}}
        :param description: 代码片段描述
        :return: 响应结果
        """
        data = {
            "access_token": self.access_token,
            "files": files,
            "description": description
        }
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data,
                timeout=1
            )
        except TimeoutError as e:
            return {}
        except BaseException as e:
            print(e)

        return response.json()

    def get_single_gist(self, gist_id):
        """
        获取单条代码片段
        :param gist_id: 代码片段ID
        :return: 响应结果
        """
        url = f"{self.base_url}/{gist_id}"
        params = {
            "access_token": self.access_token
        }
        response = requests.get(
            url,
            headers=self.headers,
            params=params
        )
        return response.json()

    def update_gist(self, gist_id, description=None, files=None):
        """
        修改代码片段
        :param gist_id: 代码片段ID
        :param description: 新的描述
        :param files: 新的文件内容
        :return: 响应结果
        """
        url = f"{self.base_url}/{gist_id}"
        data = {
            "access_token": self.access_token
        }
        if description:
            data["description"] = description
        if files:
            data["files"] = files

        response = requests.patch(
            url,
            headers=self.headers,
            json=data
        )
        return response.json()

    def delete_gist(self, gist_id):
        """
        删除指定代码片段
        :param gist_id: 代码片段ID
        :return: 响应状态码
        """
        url = f"{self.base_url}/{gist_id}"
        params = {
            "access_token": self.access_token
        }
        response = requests.delete(
            url,
            headers=self.headers,
            params=params
        )
        return response.status_code


access_token = config_instance.get('access_token')
api = GiteeGistAPI(access_token)

# try:
#     # 1. 获取代码片段列表
#     print("获取代码片段列表:")
#     gists = api.get_gists(page=1, per_page=5)
#     print(gists)
#
#     # 2. 创建代码片段
#     print("\n创建代码片段:")
#     new_gist = api.create_gist(
#         files={"test.py": {"content": "print('Hello World')"}},
#         description="这是一个测试代码片段2025年6月22日"
#     )
#     print(new_gist)
#     gist_id = new_gist.get("id")
#
#     if gist_id:
#         # 3. 获取单条代码片段
#         print("\n获取单条代码片段:")
#         single_gist = api.get_single_gist(gist_id)
#         print(single_gist)
#
#         # 4. 修改代码片段
#         print("\n修改代码片段:")
#         updated_gist = api.update_gist(
#             gist_id,
#             description="修改后的描述"
#         )
#         print(updated_gist)
#
#         # 5. 删除代码片段
#         print("\n删除代码片段:")
#         status_code = api.delete_gist(gist_id)
#         print(f"删除状态码: {status_code}")
#
# except Exception as e:
#     print(f"发生错误: {e}")