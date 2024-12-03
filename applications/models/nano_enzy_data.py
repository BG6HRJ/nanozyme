import datetime

from applications.extensions import db


class NanoEnzyData(db.Model):
    __tablename__ = 'nano_enzy_data'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    name = db.Column(db.String(255), comment='Name')
    mimic_enzyme_activity = db.Column(db.String(255), comment='Mimic Enzyme Activity')
    n = db.Column(db.Integer, comment='N')
    p = db.Column(db.Integer, comment='P')
    s = db.Column(db.Integer, comment='S')
    si = db.Column(db.Integer, comment='Si')
    se = db.Column(db.Integer, comment='Se')
    b = db.Column(db.Integer, comment='B')
    f = db.Column(db.Integer, comment='F')
    cl = db.Column(db.Integer, comment='Cl')
    br = db.Column(db.Integer, comment='Br')
    i = db.Column(db.Integer, comment='I')
    metal_ratio = db.Column(db.Float, comment='Metal ratio')
    metal_type = db.Column(db.Float, comment='Metal type')
    metal_valence = db.Column(db.Float, comment='Metal valence')
    submetal_ratio = db.Column(db.Float, comment='Submetal ratio')
    submetal_type = db.Column(db.Float, comment='Submetal type')
    submetal_valence = db.Column(db.Float, comment='Submetal valence')
    _3rd_metal_ratio = db.Column(db.Float, comment='3rd metal ratio')
    _3rd_metal_type = db.Column(db.Float, comment='3rd metal type')
    _3rd_metal_valence = db.Column(db.Float, comment='3rd metal valence')
    _4th_metal_ratio = db.Column(db.Float, comment='4th metal ratio')
    _4th_metal_type = db.Column(db.Float, comment='4th metal type')
    _4th_metal_valence = db.Column(db.Float, comment='4th metal valence')
    shape = db.Column(db.String(255), comment='shape')
    size_per_nm = db.Column(db.Float, comment='Size/nm')
    surface_modification = db.Column(db.String(255), comment='Surface modification')
    dispersion_medium = db.Column(db.String(255), comment='Dispersion medium')
    buffer_ph_value = db.Column(db.Float, comment='Buffer pH value')
    buffer_ph = db.Column(db.String(255), comment='Buffer pH')
    temperature = db.Column(db.Integer, comment='Temperature/℃')
    substrate1 = db.Column(db.String(255), comment='Substrate1')
    substrate2 = db.Column(db.String(255), comment='Substrate2 ')
    substrate2_concentration_mm = db.Column(db.Float, comment='Substrate2 concentration (mM)')
    km_per_mm = db.Column(db.Float, comment='Km/mM')
    vmax_micro_m_per_s = db.Column(db.Float, comment='Vmax/μM s-1')
    kcat_per_s = db.Column(db.Float, comment='Kcat/s-1')
    k_cat_per_Km_per_mol_per_s = db.Column(db.String(255),
                                           comment='k cat /Km (Catalytic efficiency) /M-1 s-1')
    ic50_per_micro_mol = db.Column(db.Float, comment='IC50 (SOD) /μM')
    data_reference_doi = db.Column(db.String(255), comment='data reference doi')
    path = db.Column(db.String(2048), comment='path')
    num = db.Column(db.Float, comment='num')

    username = db.Column(db.String(255), comment='username')

    status = db.Column(db.Integer, comment='Status', default=1)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='Create Time')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='Update Time')
