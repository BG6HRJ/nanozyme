import json

from flask import Blueprint, jsonify, request
from flask_login import login_required

from applications.extensions import db
from applications.models import NanoEnzyData
from applications.schemas import NanoEnzyDataSchema

bp = Blueprint('nano_enzy_data', __name__, url_prefix='/nano_enzy_data')


@bp.get('/data')
def data():
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', type=int)

    if limit > 100:
        return jsonify({"code": 200, "msg": "error"})

    query = NanoEnzyData.query.order_by(NanoEnzyData.create_time).paginate(page=page, per_page=limit, error_out=False)
    data = query.items

    res = {
        "code": 0,
        "msg": "",
        "count": query.total,
        "data": NanoEnzyDataSchema(many=True).dump(data)
    }
    return jsonify(res)


@bp.post('/data_details')
def data_details():
    # 拿到点击的details所在行数据的id
    details_id_get = request.form.get('details_id')
    query = NanoEnzyData.query.filter(NanoEnzyData.id == details_id_get).paginate()
    data = query.items

    res = {
        "code": 0,
        "msg": "",
        "count": query.total,
        "data": NanoEnzyDataSchema(many=True).dump(data)
    }
    return jsonify(res)


@bp.post('/search')
def search():
    # 拿到表单输入的数据
    search_data = request.get_json(force=True)
    input_name = search_data.get("keyword")
    cleand_input = input_name.strip()

    # 查询数据库中所有与输入匹配的行数据
    query = NanoEnzyData.query.filter(NanoEnzyData.name.ilike('%{}%'.format(cleand_input))).paginate(page=1, per_page=15, error_out=False)
    query = query.order_by(NanoEnzyData.create_time)

    # res：响应字典
    res = {
        "code": 0,
        "msg": "",
        "count": query.count(),
        "data": NanoEnzyDataSchema(many=True).dump(query)
    }
    return jsonify(res)


@bp.post('/save')
def save():
    req_json = request.get_json(force=True)

    # 初始化一个新的字典，用于存储处理后的数据
    processed_json = {}

    # 遍历 req_json 中的每个键值对
    for key, value in req_json.items():
        # 去除字符串两端的空白字符，并检查结果是否为空
        cleaned_value = value.strip()
        processed_json[key] = cleaned_value if cleaned_value != '' else None

    # processed_json 现在包含处理后的数据，其中空字符串和空格已替换为 None

    nano_enzy_data = NanoEnzyData(
        name=processed_json.get('name'),
        mimic_enzyme_activity=processed_json.get('mimic_enzyme_activity'),
        n=processed_json.get('n'),
        p=processed_json.get('p'),
        s=processed_json.get('s'),
        si=processed_json.get('si'),
        se=processed_json.get('se'),
        b=processed_json.get('b'),
        f=processed_json.get('f'),
        cl=processed_json.get('cl'),
        br=processed_json.get('br'),
        i=processed_json.get('i'),
        metal_ratio=processed_json.get('metal_ratio'),
        metal_type=processed_json.get('metal_type'),
        metal_valence=processed_json.get('metal_valence'),
        submetal_ratio=processed_json.get('submetal_ratio'),
        submetal_type=processed_json.get('submetal_type'),
        submetal_valence=processed_json.get('submetal_valence'),
        _3rd_metal_ratio=processed_json.get('_3rd_metal_ratio'),
        _3rd_metal_type=processed_json.get('_3rd_metal_type'),
        _3rd_metal_valence=processed_json.get('_3rd_metal_valence'),
        _4th_metal_ratio=processed_json.get('_4th_metal_ratio'),
        _4th_metal_type=processed_json.get('_4th_metal_type'),
        _4th_metal_valence=processed_json.get('_4th_metal_valence'),
        shape=processed_json.get('shape'),
        size_per_nm=processed_json.get('size_per_nm'),
        surface_modification=processed_json.get('surface_modification'),
        dispersion_medium=processed_json.get('dispersion_medium'),
        buffer_ph_value=processed_json.get('buffer_ph_value'),
        buffer_ph=processed_json.get('buffer_ph'),
        temperature=processed_json.get('temperature'),
        substrate1=processed_json.get('substrate1'),
        substrate2=processed_json.get('substrate2'),
        substrate2_concentration_mm=processed_json.get('substrate2_concentration_mm'),
        km_per_mm=processed_json.get('km_per_mm'),
        vmax_micro_m_per_s=processed_json.get('vmax_micro_m_per_s'),
        kcat_per_s=processed_json.get('kcat_per_s'),
        k_cat_per_Km_per_mol_per_s=processed_json.get(
            'k_cat_per_Km_per_mol_per_s'),
        ic50_per_micro_mol=processed_json.get('ic50_per_micro_m'),
        data_reference_doi=processed_json.get('data_reference_doi'),
        path=processed_json.get('path'),
        num=processed_json.get('num'),
    )

    db.session.add(nano_enzy_data)
    db.session.commit()
    return jsonify(success=True, msg="Success")


@bp.post('/json')
def json2():
    with open('data/string_mappings.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return jsonify(data)


@bp.post('/completion_data')
def completion_data():
    # 拿到点击的details所在行数据的id
    json_data = request.get_json()
    formula = json_data['Chemical_formula']
    if ':' in formula:
        formula = formula.split(':')[0].strip()

    query = NanoEnzyData.query.filter(NanoEnzyData.name == formula).paginate()
    data = query.items

    res = {
        "code": 0,
        "msg": "",
        "count": query.total,
        "data": NanoEnzyDataSchema(many=True).dump(data)
    }
    return jsonify(res)
