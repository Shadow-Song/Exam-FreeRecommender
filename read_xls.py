import pandas as pd
import numpy as np
import json


# 将*.xls格式转化为*.csv格式
def convert(filename: str):
    data_frame = pd.read_excel('./static/uploads/'+filename, 0, index_col=0)
    data_frame.to_csv('./static/data/data.csv', encoding='utf-8')


def replace(data_frame: pd):
    data_frame.loc[data_frame["综合"].isin(['优秀']), "综合"] = 90
    data_frame.loc[data_frame["综合"].isin(['良好']), "综合"] = 80
    data_frame.loc[data_frame["综合"].isin(['中等']), "综合"] = 70
    data_frame.loc[data_frame["综合"].isin(['合格']), "综合"] = 60
    data_frame.loc[data_frame["综合"].isin(['不合格']), "综合"] = 0
    data_frame.loc[data_frame["综合"].isin(['通过']), "综合"] = 85
    data_frame.loc[data_frame["综合"].isin(['不通过']), "综合"] = 0


# 获取所有学生的学号
def get_students(data_frame: pd) -> list:
    data_id = data_frame['学号']
    namelist = data_id.drop_duplicates(keep='first', inplace=False)
    # print (namelist)
    namelist_list = namelist.tolist()
    # print(namelist_list, file=data)
    # [id, id, ..., id]
    return namelist_list


# 获取一个学生的成绩信息，参数为一个学生的子数据帧
def get_one_score(sub_data_frame: pd) -> list:
    student_info = list(sub_data_frame[0])
    course_info = sub_data_frame[1].filter(items=['课程名称', '学分', '综合'])
    score = np.array(course_info)
    score = score.tolist()
    info = [student_info, score]
    # [[class_name, score, GPA], [class_name, score, GPA], ..., [class_name, score, GPA]]
    return info
    # print(student_info)
    # print(score, file=data)


# 对数据帧按照学号进行分组，传入每一组以获得信息
def get_scores(data_frame: pd) -> list:
    replace(data_frame=data_frame)
    student_groups = data_frame.groupby(['学号', '姓名'])
    score = []
    for student in student_groups:
        score.append(get_one_score(student))
    # [
    #   [id, name],
    #   [
    #       [class_name, score, GPA],
    #       [class_name, score, GPA],
    #       ...,
    #       [class_name, score, GPA]
    #   ]
    # ]
    return score
    # print(score, file=data)


def default_dump(obj):
    """Convert numpy classes to JSON serializable objects."""
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


convert('list.xls')
log = open('./static/log/result.txt', 'w+')
file = open('./static/data/data.csv')
data = pd.read_csv(file)
result = get_scores(data_frame=data)

json_file_path = './static/data/data.json'
json_file = open(json_file_path, 'w+')
# str_json = json.dumps(result, ensure_ascii=False, indent=2)

json.dump(result, json_file, indent=4, ensure_ascii=False, default=default_dump)
print(result, file=log)
