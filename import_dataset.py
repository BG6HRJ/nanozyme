import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from applications.models import NanoEnzyData

# 读取 Excel 文件
excel_file = 'data/SLP-20231010.xlsx'
df = pd.read_excel(excel_file)

# 删除列中的首尾空格
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# 将空字符替换为NaN
df.replace('', None, inplace=True)

# 连接到数据库
db_uri = 'sqlite:///./nano_enzyme.db'
engine = create_engine(db_uri)

Session = sessionmaker(bind=engine)
session = Session()

# 将数据逐行插入表中
table_name = 'nano_enzy_data'  # 替换为实际的表名
for _, row in df.iterrows():
    # 创建数据对象
    nano_enzy_data = NanoEnzyData(
        name=row[0],
        mimic_enzyme_activity=row[1],
        n=row[2],
        p=row[3],
        s=row[4],
        si=row[5],
        se=row[6],
        b=row[7],
        f=row[8],
        cl=row[9],
        br=row[10],
        i=row[11],
        metal_ratio=row[12],
        metal_type=row[13],
        metal_valence=row[14],
        submetal_ratio=row[15],
        submetal_type=row[16],
        submetal_valence=row[17],
        _3rd_metal_ratio=row[18],
        _3rd_metal_type=row[19],
        _3rd_metal_valence=row[20],
        _4th_metal_ratio=row[21],
        _4th_metal_type=row[22],
        _4th_metal_valence=row[23],
        shape=row[24],
        size_per_nm=row[25],
        surface_modification=row[26],
        dispersion_medium=row[27],
        buffer_ph_value=row[28],
        buffer_ph=row[29],
        temperature=row[30],
        substrate1=row[31],
        substrate2=row[32],
        substrate2_concentration_mm=row[33],
        km_per_mm=row[34],
        vmax_micro_m_per_s=row[35],
        kcat_per_s=row[36],
        k_cat_per_Km_per_mol_per_s=row[37],
        ic50_per_micro_mol=row[38],
        data_reference_doi=row[39],
        path=row[40],
    )

    session.add(nano_enzy_data)
    session.commit()

    print('Data: %d added' % _)

print('All Data Import OK!')
