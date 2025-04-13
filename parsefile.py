import csv
import openpyxl

def parse_file(file):
    """
    解析上传的文件内容，支持 CSV 和 Excel 格式。

    参数:
        file (FileStorage): 上传的文件对象（Flask 的 request.files 返回的对象）。

    返回:
        list: 解析后的数据（列表形式，每行数据为一个字典或元组）。

    异常:
        ValueError: 如果文件类型不受支持或解析失败。
    """
    try:
        # 获取文件名
        filename = file.filename

        # 初始化解析结果
        data = []

        # 处理 CSV 文件
        if filename.endswith('.csv'):
            # 以二进制模式读取文件并去除 NUL 字符
            binary_content = file.read()
            clean_content = binary_content.replace(b'\x00', b'')
            try:
                text_content = clean_content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text_content = clean_content.decode('gbk')
                except UnicodeDecodeError:
                    raise ValueError("无法确定文件编码")
            file.seek(0)  # 重置文件指针以便后续处理
            reader = csv.DictReader(text_content.splitlines())
            data = list(reader)
            print(f"解析后的 CSV 数据: {data}")  # 调试信息
            return data

        # 处理 Excel 文件
        elif filename.endswith(('.xlsx', '.xls')):
            try:
                workbook = openpyxl.load_workbook(file)
                sheet = workbook.active
                for row in sheet.iter_rows(values_only=True):
                    data.append(row)
                print(f"解析后的 Excel 数据: {data}")  # 调试信息
                return data
            except Exception as e:
                raise ValueError(f"Excel 文件解析失败: {str(e)}")

        # 如果文件类型不受支持
        else:
            raise ValueError("不支持的文件类型")

    except Exception as e:
        print(f"文件解析失败: {str(e)}")  # 调试信息
        raise ValueError(f"文件解析失败: {str(e)}")


