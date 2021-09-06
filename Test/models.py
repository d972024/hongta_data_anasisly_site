
from django.db import models
from django.db.models import AutoField,CharField,SmallIntegerField,FloatField,DateTimeField
# Create your models here.

class Fact_act_hscb(models.Model):
    md5_id=CharField(max_length=100,primary_key=True)
    billno=CharField(max_length=50,db_column='单据编号')
    typed=CharField(max_length=50,db_column='类型',null=True)
    prod_pack=CharField(max_length=100,db_column='产品或组件',null=True)
    unit_name=CharField(max_length=50,db_column='基本单位',null=True)
    qty=FloatField(db_column='数量',null=True)
    amount=FloatField(db_column='成本',null=True)
    gd_id=CharField(db_column='生产工单',max_length=100,null=True)
    cost_id=CharField(db_column='成本核算对象编码',max_length=100,null=True)
    factory_id=CharField(db_column='工厂',max_length=50,null=True)
    work_center=CharField(db_column='工作中心',max_length=50,null=True)
    bill_type=CharField(db_column='单据类型',max_length=100,null=True)
    business_date=DateTimeField(db_column='日期',null=True)
    product_code=CharField(db_column='产品编码',max_length=100,null=True)
    product_name=CharField(db_column='产品名称',max_length=100,null=True)
    product_unit=CharField(db_column='产品单位',max_length=100,null=True)

    def __str__(self):
        return self.md5_id