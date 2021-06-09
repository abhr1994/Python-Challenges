from pyspark.sql.functions import explode, col,regexp_replace,concat,when
import pyspark.sql.functions as f
from pyspark.sql.types import StructType,StructField,StringType,ArrayType,LongType,DoubleType
import sys,os
from distutils.util import strtobool

def delete_junk_files(csv_dir):
    for root, dirs, files in os.walk("/dbfs"+csv_dir):
        for filename in files:
            if filename.startswith(('_SUCCESS', '_committed', '_started')):
                print("Deleting {}".format(filename))
                dbutils.fs.rm(os.path.join(csv_dir, filename))

def create_partymasteramn_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln']

    df2 = df1.select(*columns)
    for item in schema:
        if not item in df2.columns:
            df2 = df2.withColumn(item, f.lit(''))

    for item in df2.schema.fields:
        if isinstance(item.dataType, StringType):
            df2 = df2.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    target_path = os.path.join(csv_dir, "partymasteramn")
    df2.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_qualification_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'inst_nm', 'cntry', 'qlfctn_type', 'qlfctn_nm', 'qualification_id', 'city', 'qlfctn_abbrv_nm',
              'eff_end_dt', 'qlfctn_sts', 'state', 'eff_strt_dt','primary_key']

    df2 = df1.select(*columns, explode("qualifications.qualification").alias("qualification"))
    df3 = df2.select(*columns, "qualification.*")
    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("qualification_id").isNotNull(), col("qualification_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "qualification")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_alternativeid_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'issng_auth', 'eff_end_dt', 'alt_id', 'alt_id_val', 'eff_strt_dt', 'alt_id_type','primary_key']

    df2 = df1.select(*columns, explode("alternativeids.alternative_id").alias("alternative_id"))
    df3 = df2.select(*columns, "alternative_id.*")
    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("alt_id").isNotNull(),
                                                    col("alt_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "alternative_id")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_department_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'department_id', 'division_nm','primary_key']

    df2 = df1.select(*columns, explode("departments.department").alias("department"))
    df3 = df2.select(*columns, "department.*")

    for item in schema:
        if not item in df2.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("department_id").isNotNull(),
                                                    col("department_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "department")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_departmentunits_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'status', 'unit_id', 'last_update', 'cost_center_id', 'department_id', 'department_nm','primary_key']

    df2 = df1.select(*columns, explode("departmentunits.department_unit").alias("department_unit"))
    df3 = df2.select(*columns, "department_unit.*")

    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("department_id").isNotNull(),
                                                    col("department_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "department_unit")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_electronic_address_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr_1', 'phn_num', 'gln',
              'pref_lvl', 'elec_addr', 'opt_out_ind', 'eff_end_date', 'sts_cd', 'slctbl_ind', 'elec_addr_id',
              'elec_addr_type', 'is_vld', 'usg_type', 'full_elec_addr', 'eff_strt_date','primary_key']

    df2 = df1.select(*columns,explode("electronicaddresses.electronic_address").alias("electronic_address")).withColumnRenamed("full_elec_addr", "full_elec_addr_1")

    def change(f):
        if f == "full_elec_addr":
            return "full_elec_addr_1"
        else:
            return f

    columns = [change(i) for i in columns]

    df3 = df2.select(*columns, "electronic_address.*")
    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("elec_addr_id").isNotNull(),
                                                    col("elec_addr_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "electronic_address")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_license_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'lcns_issue_dt', 'lcns_cntry', 'lcns_state', 'lcns_brd', 'lcns_type', 'license_id', 'lcns_exprtn_dt',
              'lcns_num', 'lcns_sts', 'lcns_dt_verified','primary_key']

    df2 = df1.select(*columns, explode("licenses.license").alias("license"))
    df3 = df2.select(*columns, "license.*")

    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("license_id").isNotNull(),
                                                    col("license_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "license")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_emergency_contact_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm_1', 'party_sub_type', 'prfx_nm', 'frst_nm_1',
              'mdl_nm', 'lst_nm_1', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'relationship', 'addr_line', 'emergency_id', 'frst_nm', 'city', 'zip', 'work_phone', 'state',
              'home_phone', 'full_nm', 'cell_phone', 'lst_nm','primary_key']

    df2 = df1.select(*columns, explode("emergencycontacts.emergency_contact").alias("emergency_contact")).withColumnRenamed("full_nm", "full_nm_1").withColumnRenamed("frst_nm", "frst_nm_1").withColumnRenamed("lst_nm", "lst_nm_1")
    def change(f):
        if f == "full_nm":
            return "full_nm_1"
        elif f == "frst_nm":
            return "frst_nm_1"
        elif f == "lst_nm":
            return "lst_nm_1"
        else:
            return f

    columns = [change(i) for i in columns]
    df3 = df2.select(*columns, "emergency_contact.*")

    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("emergency_id").isNotNull(),
                                                    col("emergency_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "emergency_contact")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_postal_address_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'raw_addr_ln_1', 'address_type_ind', 'postal_bar_cd', 'pre_directional', 'street_nm', 'cntry', 'county',
              'location_coord_desc', 'raw_addr_ln_2', 'enrichment_sts', 'post_directional', 'residence_nm',
              'street_sfx', 'postal_cd', 'street_num', 'validation_sts_cd', 'city', 'raw_postal_cd',
              'mailability_score_type', 'postal_cd_ext', 'raw_state', 'longitude', 'addr_type', 'state',
              'validation_message', 'addr_id', 'building_nm', 'latitude', 'raw_city', 'addr_ln_4', 'addr_ln_5',
              'addr_ln_2', 'addr_ln_3', 'deliverable_ind', 'addr_ln_1','primary_key']

    df2 = df1.select(*columns, explode("postaladdresses.postal_address").alias("postal_address"))
    df3 = df2.select(*columns, "postal_address.*")

    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("addr_id").isNotNull(),
                                                    col("addr_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "postal_address")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_ethnicity_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'ethnicity_id', 'ethnicity','primary_key']

    df2 = df1.select(*columns, explode("ethnicities.ethnicity").alias("ethnicity"))
    df3 = df2.select(*columns, "ethnicity.*")

    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("ethnicity_id").isNotNull(),
                                                    col("ethnicity_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "ethnicity")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_gender_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'gender_id', 'gndr_cd','primary_key']

    df2 = df1.select(*columns, explode("genders.gender").alias("gender"))
    df3 = df2.select(*columns, "gender.*")

    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("gender_id").isNotNull(),
                                                    col("gender_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "gender")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_language_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'language_id', 'lang_cd', 'pref_lvl','primary_key']

    df2 = df1.select(*columns, explode("languages.language").alias("language"))
    df3 = df2.select(*columns, "language.*")

    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("language_id").isNotNull(),
                                                    col("language_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "language")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_party_name_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm_1', 'party_sub_type', 'prfx_nm', 'frst_nm_1',
              'mdl_nm_1', 'lst_nm_1', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'party_nm_id', 'nm_type', 'full_nm', 'frst_nm', 'mdl_nm', 'lst_nm', 'eff_strt_dt', 'eff_end_dt','primary_key']

    def change(f):
        if f == "full_nm":
            return "full_nm_1"
        elif f == "frst_nm":
            return "frst_nm_1"
        elif f == "lst_nm":
            return "lst_nm_1"
        elif f == "mdl_nm":
            return "mdl_nm_1"
        else:
            return f

    df2 = df1.select(*columns, explode("partynames.party_name").alias("party_name")).withColumnRenamed("full_nm", "full_nm_1").withColumnRenamed("frst_nm", "frst_nm_1").withColumnRenamed("lst_nm", "lst_nm_1").withColumnRenamed("mdl_nm", "mdl_nm_1")
    columns = [change(i) for i in columns]
    df3 = df2.select(*columns, "party_name.*")
    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("party_nm_id").isNotNull(),
                                                    col("party_nm_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "party_name")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_phone_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num_1', 'gln',
              'slctbl_ind', 'vldtn_msg', 'cmnts', 'eff_strt_dt', 'eff_end_dt', 'sts_cd', 'pref_lvl', 'usg_type',
              'avlvlty_prd', 'phn_type', 'phone_id', 'phn_num', 'phn_num_ext', 'opt_out_ind','primary_key']

    def change(f):
        if f == "phn_num":
            return "phn_num_1"
        else:
            return f
    df2 = df1.select(*columns, explode("phones.phone").alias("phone")).withColumnRenamed("phn_num", "phn_num_1")
    columns = [change(i) for i in columns]
    df3 = df2.select(*columns, "phone.*")
    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("phone_id").isNotNull(),
                                                    col("phone_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "phone")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_role_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'status_type', 'role_id', 'role_type', 'classif_cd','primary_key']

    df2 = df1.select(*columns, explode("roles.role").alias("role"))
    df3 = df2.select(*columns, "role.*")
    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("role_id").isNotNull(),
                                                    col("role_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "role")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def create_specialty_csv(df1,columns,csv_dir,mode):
    schema = ['createddate', 'updateddate', 'grid', 'party_type', 'full_nm', 'party_sub_type', 'prfx_nm', 'frst_nm',
              'mdl_nm', 'lst_nm', 'defintive_id', 'duns_site_number', 'ctznshp', 'ssn', 'birth_dt', 'state_of_birth',
              'country_of_birth', 'city_of_birth', 'mrtl_sts', 'patient_cnfdntlty_ind', 'dsblty_ind', 'chldrn_cnt',
              'death_dt', 'foundation_dt', 'foundation_yr', 'state_of_incorp', 'country_of_incorp', 'emp_cnt',
              'no_solicite_flag', 'no_contract_flag', 'sfx_nm', 'spclty_type', 'full_elec_addr', 'phn_num', 'gln',
              'spclty_cd', 'certs_sts', 'cert_brd', 'sub_spclty_cd', 'specialty_id', 'spclty_prefrnc', 'classfctn','primary_key']

    df2 = df1.select(*columns, explode("specialties.specialty").alias("specialty"))
    df3 = df2.select(*columns, "specialty.*")
    for item in schema:
        if not item in df3.columns:
            df3 = df3.withColumn(item, f.lit(''))

    for item in df3.schema.fields:
        if isinstance(item.dataType, StringType):
            df3 = df3.withColumn(item.name, regexp_replace(col(item.name), "[\\r\\n\\t]", ""))

    df3 = df3.withColumn("primary_key", concat(when(col("grid").isNotNull(), col("grid")).otherwise(f.lit("")),
                                               when(col("specialty_id").isNotNull(),
                                                    col("specialty_id")).otherwise(
                                                   f.lit(""))))
    target_path = os.path.join(csv_dir, "specialty")
    df3.select(*schema).repartition(1).write.mode(mode.strip()).format("csv").option("header", "true").option("emptyValue", '').option("sep", ",").save(target_path)
    delete_junk_files(target_path)

def xml_files_in_directory(xml_dir):
    dbutils.fs.rm("/FileStore/tables/xml_files/",True)
    dbutils.fs.mkdirs("/FileStore/tables/xml_files/")
    import fnmatch, os
    pattern = 'PartyMasterAMN*.xml'
    print('Pattern :', pattern)
    print()
    path = "/dbfs"+xml_dir
    files = os.listdir(path)
    for name in files:
        print('Filename: %-25s %s' % (name, fnmatch.fnmatch(name, pattern)))
        if fnmatch.fnmatch(name, pattern):
            dbutils.fs.cp(os.path.join(xml_dir, name),os.path.join("/FileStore/tables/xml_files/",name))



def partymaster(xml_dir,csv_dir,mode,rowtag,only_xmls,batch):
    try:
        schema_of_table = StructType([StructField("partymasteramn", ArrayType(StructType([StructField("_createddate", StringType(), True), StructField("_updateddate", StringType(), True), StructField("alternativeids", StructType([StructField("alternative_id", ArrayType(StructType([StructField("alt_id", StringType(), True), StructField("alt_id_type", StringType(), True), StructField("alt_id_val", StringType(), True), StructField("eff_end_dt", StringType(), True), StructField("eff_strt_dt", StringType(), True), StructField("issng_auth", StringType(), True)]), True), True)]), True), StructField("birth_dt", StringType(), True), StructField("city_of_birth", StringType(), True), StructField("country_of_birth", StringType(), True), StructField("ctznshp", StringType(), True), StructField("departments", StructType([StructField("department", ArrayType(StructType([StructField("department_id", StringType(), True), StructField("division_nm", StringType(), True)]), True), True)]), True), StructField("departmentunits", StructType([StructField("department_unit", ArrayType(StructType([StructField("cost_center_id", StringType(), True), StructField("department_id", StringType(), True), StructField("department_nm", StringType(), True), StructField("last_update", StringType(), True), StructField("status", StringType(), True), StructField("unit_id", StringType(), True)]), True), True)]), True), StructField("defintive_id", StringType(), True), StructField("duns_site_number", StringType(), True), StructField("electronicaddresses", StructType([StructField("electronic_address", ArrayType(StructType([StructField("eff_end_date", StringType(), True), StructField("eff_strt_date", StringType(), True), StructField("elec_addr", StringType(), True), StructField("elec_addr_id", StringType(), True), StructField("elec_addr_type", StringType(), True), StructField("full_elec_addr", StringType(), True), StructField("is_vld", StringType(), True), StructField("opt_out_ind", StringType(), True), StructField("pref_lvl", StringType(), True), StructField("slctbl_ind", StringType(), True), StructField("sts_cd", StringType(), True), StructField("usg_type", StringType(), True)]), True), True)]), True), StructField("emergencycontacts", StructType([StructField("emergency_contact", ArrayType(StructType([StructField("addr_line", StringType(), True), StructField("cell_phone", StringType(), True), StructField("city", StringType(), True), StructField("emergency_id", StringType(), True), StructField("frst_nm", StringType(), True), StructField("full_nm", StringType(), True), StructField("home_phone", StringType(), True), StructField("lst_nm", StringType(), True), StructField("relationship", StringType(), True), StructField("state", StringType(), True), StructField("work_phone", StringType(), True), StructField("zip", StringType(), True)]), True), True)]), True), StructField("emp_cnt", DoubleType(), True), StructField("ethnicities", StructType([StructField("ethnicity", ArrayType(StructType([StructField("ethnicity", StringType(), True), StructField("ethnicity_id", StringType(), True)]), True), True)]), True), StructField("frst_nm", StringType(), True), StructField("full_elec_addr", StringType(), True), StructField("full_nm", StringType(), True), StructField("genders", StructType([StructField("gender", ArrayType(StructType([StructField("gender_id", StringType(), True), StructField("gndr_cd", StringType(), True)]), True), True)]), True), StructField("grid", StringType(), True), StructField("languages", StructType([StructField("language", ArrayType(StructType([StructField("lang_cd", StringType(), True), StructField("language_id", StringType(), True), StructField("pref_lvl", StringType(), True)]), True), True)]), True), StructField("licenses", StructType([StructField("license", ArrayType(StructType([StructField("lcns_brd", StringType(), True), StructField("lcns_cntry", StringType(), True), StructField("lcns_exprtn_dt", StringType(), True), StructField("lcns_issue_dt", StringType(), True), StructField("lcns_num", StringType(), True), StructField("lcns_state", StringType(), True), StructField("lcns_sts", StringType(), True), StructField("lcns_type", StringType(), True), StructField("license_id", StringType(), True)]), True), True)]), True), StructField("lst_nm", StringType(), True), StructField("mdl_nm", StringType(), True), StructField("mrtl_sts", StringType(), True), StructField("no_contract_flag", StringType(), True), StructField("party_sub_type", StringType(), True), StructField("party_type", StringType(), True), StructField("partynames", StructType([StructField("party_name", ArrayType(StructType([StructField("eff_end_dt", StringType(), True), StructField("eff_strt_dt", StringType(), True), StructField("frst_nm", StringType(), True), StructField("full_nm", StringType(), True), StructField("lst_nm", StringType(), True), StructField("mdl_nm", StringType(), True), StructField("nm_type", StringType(), True), StructField("party_nm_id", StringType(), True)]), True), True)]), True), StructField("phn_num", StringType(), True), StructField("phones", StructType([StructField("phone", ArrayType(StructType([StructField("avlvlty_prd", StringType(), True), StructField("cmnts", StringType(), True), StructField("eff_end_dt", StringType(), True), StructField("eff_strt_dt", StringType(), True), StructField("opt_out_ind", StringType(), True), StructField("phn_num", StringType(), True), StructField("phn_num_ext", StringType(), True), StructField("phn_type", StringType(), True), StructField("phone_id", StringType(), True), StructField("pref_lvl", StringType(), True), StructField("slctbl_ind", StringType(), True), StructField("sts_cd", StringType(), True), StructField("usg_type", StringType(), True), StructField("vldtn_msg", StringType(), True)]), True), True)]), True), StructField("postaladdresses", StructType([StructField("postal_address", ArrayType(StructType([StructField("addr_id", StringType(), True), StructField("addr_ln_1", StringType(), True), StructField("addr_ln_2", StringType(), True), StructField("addr_ln_3", StringType(), True), StructField("addr_ln_4", StringType(), True), StructField("addr_ln_5", StringType(), True), StructField("addr_type", StringType(), True), StructField("address_type_ind", StringType(), True), StructField("building_nm", StringType(), True), StructField("city", StringType(), True), StructField("cntry", StringType(), True), StructField("county", StringType(), True), StructField("deliverable_ind", StringType(), True), StructField("enrichment_sts", StringType(), True), StructField("latitude", StringType(), True), StructField("location_coord_desc", StringType(), True), StructField("longitude", StringType(), True), StructField("mailability_score_type", StringType(), True), StructField("post_directional", StringType(), True), StructField("postal_bar_cd", StringType(), True), StructField("postal_cd", StringType(), True), StructField("postal_cd_ext", StringType(), True), StructField("pre_directional", StringType(), True), StructField("raw_addr_ln_1", StringType(), True), StructField("raw_addr_ln_2", StringType(), True), StructField("raw_city", StringType(), True), StructField("raw_postal_cd", StringType(), True), StructField("raw_state", StringType(), True), StructField("residence_nm", StringType(), True), StructField("state", StringType(), True), StructField("street_nm", StringType(), True), StructField("street_num", StringType(), True), StructField("street_sfx", StringType(), True), StructField("validation_message", StringType(), True), StructField("validation_sts_cd", StringType(), True)]), True), True)]), True), StructField("prfx_nm", StringType(), True), StructField("qualifications", StructType([StructField("qualification", ArrayType(StructType([StructField("city", StringType(), True), StructField("cntry", StringType(), True), StructField("eff_end_dt", StringType(), True), StructField("eff_strt_dt", StringType(), True), StructField("inst_nm", StringType(), True), StructField("qlfctn_abbrv_nm", StringType(), True), StructField("qlfctn_nm", StringType(), True), StructField("qlfctn_sts", StringType(), True), StructField("qlfctn_type", StringType(), True), StructField("qualification_id", StringType(), True), StructField("state", StringType(), True)]), True), True)]), True), StructField("roles", StructType([StructField("role", ArrayType(StructType([StructField("classif_cd", StringType(), True), StructField("role_id", StringType(), True), StructField("role_type", StringType(), True), StructField("status_type", StringType(), True)]), True), True)]), True), StructField("sfx_nm", StringType(), True), StructField("specialties", StructType([StructField("specialty", ArrayType(StructType([StructField("cert_brd", StringType(), True), StructField("certs_sts", StringType(), True), StructField("classfctn", StringType(), True), StructField("spclty_cd", StringType(), True), StructField("spclty_prefrnc", StringType(), True), StructField("specialty_id", StringType(), True), StructField("sub_spclty_cd", StringType(), True)]), True), True)]), True), StructField("ssn", StringType(), True), StructField("state_of_birth", StringType(), True), StructField("patient_cnfdntlty_ind", StringType(), True), StructField("dsblty_ind", StringType(), True), StructField("chldrn_cnt", DoubleType(), True), StructField("death_dt", StringType(), True), StructField("foundation_dt", StringType(), True), StructField("foundation_yr", StringType(), True), StructField("state_of_incorp", StringType(), True), StructField("country_of_incorp", StringType(), True), StructField("no_solicite_flag", StringType(), True), StructField("spclty_type", StringType(), True), StructField("gln", StringType(), True)]), True), True)])
        spark.conf.set("spark.hadoop.mapreduce.input.fileinputformat.input.dir.recursive", "true")
        spark.conf.set("spark.hive.mapred.supports.subdirectories", "true")
        if strtobool(only_xmls):
            print("Reading only the XML files present in the directory {}".format(xml_dir))
            xml_files_in_directory(xml_dir)
            xmldata = spark.read.format('com.databricks.spark.xml').option("rowTag", rowtag.strip()).load("/FileStore/tables/xml_files/",schema=schema_of_table)
            print("Data successfully read from {}".format(xml_dir))
        else:
            xmldata = spark.read.format('com.databricks.spark.xml').option("rowTag", rowtag.strip()).load(xml_dir,schema=schema_of_table)
            print("Data successfully read from {}".format(xml_dir))
        #from pyspark.sql.functions import input_file_name
        #df = df.withColumn("file_name",input_file_name())
        df = xmldata.select(explode("partymasteramn"))
        df1 = df.select("col.*").withColumnRenamed("_createddate", "createddate").withColumnRenamed("_updateddate","updateddate")
        columns = []
        for item in df1.schema.fields:
            if isinstance(item.dataType, StringType) or isinstance(item.dataType, LongType) or isinstance(item.dataType, DoubleType):
                columns.append(item.name)
        df1.cache()

        if batch == "1":
            print("Creating Partymasteramn CSV files")
            create_partymasteramn_csv(df1,columns,csv_dir,mode)
            print("Created Partymasteramn CSV files")
            print("Creating Qualification CSV files")
            create_qualification_csv(df1, columns, csv_dir, mode)
            print("Created Qualification CSV files")
            print("Creating Alternative ID CSV files")
            create_alternativeid_csv(df1, columns, csv_dir, mode)
            print("Created Alternative ID CSV files")
            print("Creating Department CSV files")
            create_department_csv(df1, columns, csv_dir, mode)
            print("Created Department CSV files")
        elif batch == "2":
            print("Creating Departmentunits CSV files")
            create_departmentunits_csv(df1, columns, csv_dir, mode)
            print("Created Departmentunits CSV files")
            print("Creating Electronic Address CSV files")
            create_electronic_address_csv(df1, columns, csv_dir, mode)
            print("Created Electronic Address CSV files")
            print("Creating License CSV files")
            create_license_csv(df1, columns, csv_dir, mode)
            print("Created License CSV files")
            print("Creating Emergency Contact CSV files")
            create_emergency_contact_csv(df1, columns, csv_dir, mode)
            print("Created Emergency Contact CSV files")
        elif batch == "3":
            print("Creating Postal Address CSV files")
            create_postal_address_csv(df1, columns, csv_dir, mode)
            print("Created Postal Address CSV files")
            print("Creating Ethnicity CSV files")
            create_ethnicity_csv(df1, columns, csv_dir, mode)
            print("Created Ethnicity CSV files")
            print("Creating Gender CSV files")
            create_gender_csv(df1, columns, csv_dir, mode)
            print("Created Gender CSV files")
            print("Creating Language CSV files")
            create_language_csv(df1, columns, csv_dir, mode)
        elif batch == "4":
            print("Created Language CSV files")
            print("Creating Party Name CSV files")
            create_party_name_csv(df1, columns, csv_dir, mode)
            print("Created Party Name CSV files")
            print("Creating Phone CSV files")
            create_phone_csv(df1, columns, csv_dir, mode)
            print("Created Phone CSV files")
            print("Creating Role CSV files")
            create_role_csv(df1, columns, csv_dir, mode)
            print("Created Role CSV files")
            print("Creating Specialty CSV files")
            create_specialty_csv(df1, columns, csv_dir, mode)
            print("Created Specialty CSV files")
        elif batch == "all":
            print("Creating Partymasteramn CSV files")
            create_partymasteramn_csv(df1, columns, csv_dir, mode)
            print("Created Partymasteramn CSV files")
            print("Creating Qualification CSV files")
            create_qualification_csv(df1, columns, csv_dir, mode)
            print("Created Qualification CSV files")
            print("Creating Alternative ID CSV files")
            create_alternativeid_csv(df1, columns, csv_dir, mode)
            print("Created Alternative ID CSV files")
            print("Creating Department CSV files")
            create_department_csv(df1, columns, csv_dir, mode)
            print("Created Department CSV files")
            print("Creating Departmentunits CSV files")
            create_departmentunits_csv(df1, columns, csv_dir, mode)
            print("Created Departmentunits CSV files")
            print("Creating Electronic Address CSV files")
            create_electronic_address_csv(df1, columns, csv_dir, mode)
            print("Created Electronic Address CSV files")
            print("Creating License CSV files")
            create_license_csv(df1, columns, csv_dir, mode)
            print("Created License CSV files")
            print("Creating Emergency Contact CSV files")
            create_emergency_contact_csv(df1, columns, csv_dir, mode)
            print("Created Emergency Contact CSV files")
            print("Creating Postal Address CSV files")
            create_postal_address_csv(df1, columns, csv_dir, mode)
            print("Created Postal Address CSV files")
            print("Creating Ethnicity CSV files")
            create_ethnicity_csv(df1, columns, csv_dir, mode)
            print("Created Ethnicity CSV files")
            print("Creating Gender CSV files")
            create_gender_csv(df1, columns, csv_dir, mode)
            print("Created Gender CSV files")
            print("Creating Language CSV files")
            create_language_csv(df1, columns, csv_dir, mode)
            print("Created Language CSV files")
            print("Creating Party Name CSV files")
            create_party_name_csv(df1, columns, csv_dir, mode)
            print("Created Party Name CSV files")
            print("Creating Phone CSV files")
            create_phone_csv(df1, columns, csv_dir, mode)
            print("Created Phone CSV files")
            print("Creating Role CSV files")
            create_role_csv(df1, columns, csv_dir, mode)
            print("Created Role CSV files")
            print("Creating Specialty CSV files")
            create_specialty_csv(df1, columns, csv_dir, mode)
            print("Created Specialty CSV files")
        else:
            pass
    except Exception as e:
        print(str(e))
        raise Exception(str(e))

def partymasterrelationship():
    pass


def main():
    if len(sys.argv) == 8:
        xml_dir=sys.argv[1]
        csv_dir=sys.argv[2]
        mode=sys.argv[3]
        rowtag = sys.argv[4]
        source_name=sys.argv[5]
        only_xmls = sys.argv[6]
        batch = sys.argv[7]

        if source_name.lower() == "partymaster":
            print("Got source name as partymaster!!!")
            print("The cmdline arguments are ")
            print(sys.argv)
            partymaster(xml_dir,csv_dir,mode,rowtag,only_xmls,batch)
        elif source_name.lower() == "partymasterrelationship":
            print("Got source name as partymasterrelationship")
            partymasterrelationship()
        else:
            print("Invalid source name passed")

    else:
        print("Insufficient or more arguments passed")
        sys.exit(1)

main()