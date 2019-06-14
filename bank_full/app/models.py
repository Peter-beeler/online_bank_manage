# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField, \
    UUIDField, ForeignKeyField,FloatField,DateField,DateTimeField, CompositeKey
import json
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from conf.config import config
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


# =========== Update Model ===============
class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)


# 管理员工号
class User(UserMixin, BaseModel):
    username = CharField()  # 用户名
    password = CharField()  # 密码
    fullname = CharField()  # 真实性名
    email = CharField()  # 邮箱
    phone = CharField()  # 电话
    status = BooleanField(default=True)  # 生效失效标识

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


# 通知人配置
class CfgNotify(BaseModel):
    check_order = IntegerField()  # 排序
    notify_type = CharField()  # 通知类型：MAIL/SMS
    notify_name = CharField()  # 通知人姓名
    notify_number = CharField()  # 通知号码
    status = BooleanField(default=True)  # 生效失效标识



# ==== entity =======
class Branch(BaseModel):
    """
    支行类
    """

    branchName = UUIDField(primary_key=True)
    branchCity = UUIDField()
    branchAsset = UUIDField()

    class Meta:
        tablename = 'branch'

class Department(BaseModel):
    """
    部门类
    """

    branchName = ForeignKeyField(Branch)
    deptId = IntegerField()
    deptName = UUIDField()
    deptType = UUIDField()
    deptManagerID = UUIDField()

    class Meta:
        tablename = 'department'
        primary_key = CompositeKey('branchName', 'deptId')

class ChequeAccount(BaseModel):
    """
    支票账户类
    """

    id = UUIDField(primary_key=True)
    branchName = ForeignKeyField(Branch)
    accountBalance = FloatField()
    openTime = DateTimeField()
    visitTime = DateTimeField()
    creditLimit = FloatField()

    class Meta:
        tablename = 'chequeaccount'

class DepositAccount(BaseModel):
    """
    储蓄账户类
    """
    id = UUIDField(primary_key=True)
    branchName = ForeignKeyField(Branch)
    accountBalance = FloatField()
    openTime = DateTimeField()
    visitTime = DateTimeField()
    interestRate = FloatField()
    currencyType = UUIDField()


    class Meta:
        tablename = 'depositaccount'

class Staff(BaseModel):
    """
    员工类
    """

    id = UUIDField(primary_key=True)
    branchName = UUIDField()
    deptId = IntegerField()
    staffName = UUIDField()
    staffPhone = UUIDField()
    staffAddr = UUIDField()
    startDate = DateField()

    class Meta:
        tablename = 'staff'

class Client(BaseModel):
    """
    客户类
    """

    id = UUIDField(primary_key=True)
    clientName = UUIDField()
    clientPhone = UUIDField()
    clientAddr = UUIDField()
    contactName = UUIDField()
    contactPhone = UUIDField()
    contactEmail = UUIDField()
    contactRelation = UUIDField()

    class Meta:
        tablename = 'client'

class Loan(BaseModel):
    """
    贷款类
    """

    branchName = ForeignKeyField(Branch)
    loanId = UUIDField()
    loanAmount = FloatField()
    payNum = IntegerField()


    class Meta:
        tablename = 'loan'
        primary_key = CompositeKey('branchName', 'loanId')

class Grant(BaseModel):
    """
    单次付款类
    """

    branchName = UUIDField()
    loanId = UUIDField()
    grantCount = IntegerField()
    grantTime = DateField()
    grantMoney = FloatField()


    class Meta:
        tablename = 'grant'
        primary_key = CompositeKey('branchName', 'loanId', 'grantCount')


# ===== relationship ======
class OpenDepositAccount(BaseModel):
    """
    开设储蓄账户
    """

    accountId = ForeignKeyField(DepositAccount)
    clientId = ForeignKeyField(Client)

    class Meta:
        tablename = 'opendepositaccount'
        primary_key = CompositeKey('accountId', 'clientId')
class OpenChequeAccount(BaseModel):
    """
    开设支票账户
    """

    accountId = ForeignKeyField(ChequeAccount)
    clientId = ForeignKeyField(Client)

    class Meta:
        tablename = 'openchequeaccount'
        primary_key = CompositeKey('accountId', 'clientId')
class ServiceRelationship(BaseModel):
    """
    业务关系，描述客户与银行的联系
    """

    branchName = ForeignKeyField(Branch)
    clientId = ForeignKeyField(Client)

    class Meta:
        tablename = 'servicerelationship'
        primary_key = CompositeKey('branchName', 'clientId')

class OpenAccount(BaseModel):
    """
    开户
    用户每开设一个支票账户或储蓄账户的同时也需要在此处创建一条记录。
    其用处为一个客户在一个支行只能开设一个储蓄账户和一个支票账户。
    该类的目的不在于查询，只在于实施该限制
    """

    branchName = ForeignKeyField(Branch)
    id = ForeignKeyField(Client)
    depositAccountId = UUIDField()
    chequeAccountId = UUIDField()

    class Meta:
        tablename = 'openaccount'
        primary_key = CompositeKey('branchName', 'id')

class OwnLoan(BaseModel):
    """
    拥有。客户拥有贷款的关系
    """

    branchName = UUIDField()
    loanId = UUIDField()
    clientId = ForeignKeyField(Client)

    class Meta:
        tablename = 'ownloan'
        primary_key = CompositeKey('branchName', 'loanId', 'clientId')

class Serve(BaseModel):
    """
    服务。员工服务客户的关系。
    """

    clientId = ForeignKeyField(Client)
    staffId = ForeignKeyField(Staff)
    ServiceType = UUIDField()

    class Meta:
        tablename = 'serve'
        primary_key = CompositeKey('clientId', 'staffId')


# =============== Database =================

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))


# 建表
def create_table():
    db.connect()
    db.create_tables([Branch, Department,Staff,Client])
    db.create_tables([ChequeAccount,DepositAccount,Loan,Grant])
    db.create_tables([OpenDepositAccount,OpenChequeAccount,ServiceRelationship,OpenAccount,OwnLoan,Serve])


if __name__ == '__main__':
    create_table()
