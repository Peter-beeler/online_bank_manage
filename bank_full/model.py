# -*- coding: utf-8 -*-
from bank import db


# ==== entity =======
class Branch(db.Model):
    """
    支行类
    """
    branchName = db.Column(db.String(20), primary_key=True)
    branchCity = db.Column(db.String(20), nullable=True)
    branchAsset = db.Column(db.Integer)

    def __init__(self, branchName, branchCity = None, branchAsset = 0):
        self.branchName = branchName
        self.branchCity = branchCity
        self.branchAsset = branchAsset

    def update(self):
        # 更新该对象的属性。需要时再实现
        pass

class Department(db.Model):
    """
    部门类
    """
    branchName = db.Column(db.String(20), db.ForeignKey('Branch.branchName'))
    deptId = db.Column(db.Integer)
    deptName = db.Column(db.String(20))
    deptType = db.Column(db.String(20), nullable = True)
    deptManagerID = db.Column(db.String(20),unique=True, nullable = True)
    __table_args__ = (
        db.PrimaryKeyConstraint('branchName', 'deptId', name='PK_Dept'),
    )

    def __init__(self, branchName, deptId, deptName, deptType = None, deptManagerID = None):
        self.branchName = branchName
        self.deptId = deptId
        self.deptName = deptName
        self.deptType = deptType
        self.deptManagerID = deptManagerID


class ChequeAccount(db.Model):
    """
    支票账户类
    """
    id = db.Column(db.String(20), primary_key=True)
    branchName = db.Column(db.String(20), db.ForeignKey('Branch.branchName'))
    accountBalance = db.Column(db.Float)
    openTime = db.Column(db.DateTime)
    visitTime = db.Column(db.DateTime)
    creditLimit = db.Column(db.Float)

    def __init__(self, branchName, deptId):
        self.branchName = branchName
        self.deptId = deptId

class DepositAccount(db.Model):
    """
    储蓄账户类
    """
    id = db.Column(db.String(20), primary_key=True)
    branchName = db.Column(db.String(20), db.ForeignKey('Branch.branchName'))
    accountBalance = db.Column(db.Float)
    openTime = db.Column(db.DateTime)
    visitTime = db.Column(db.DateTime)
    interestRate = db.Column(db.Float)
    currencyType = db.Column(db.String(20))


class Staff(db.Model):
    """
    员工类
    """
    id = db.Column(db.String(20), primary_key=True)
    branchName = db.Column(db.String(20))
    deptId = db.Column(db.Integer)
    staffName = db.Column(db.String(20))
    staffPhone = db.Column(db.String(20))
    staffAddr = db.Column(db.String(40))
    startTime = db.Column(db.Date)

    __table_args__ = (
        db.ForeignKeyConstraint(['branchName', 'deptId'], ['Department.branchName', 'Department.deptId']),
    )


class Client(db.Model):
    """
    客户类
    """
    id = db.Column(db.String(20), primary_key=True)
    clientName = db.Column(db.String(20))
    clientPhone = db.Column(db.String(20))
    clientAddr = db.Column(db.String(40))
    contactName = db.Column(db.String(20))
    contactPhone = db.Column(db.String(20))
    contactEmail = db.Column(db.String(40))
    contactRelation = db.Column(db.String(10))


class Loan(db.Model):
    """
    贷款类
    """
    branchName = db.Column(db.String(20), db.ForeignKey('Branch.branchName'))
    loanId = db.Column(db.String(6))
    loanAmount = db.Column(db.Float)
    payNum = db.Column(db.Integer)
    __table_args__ = (
        db.PrimaryKeyConstraint('branchName', 'loanId', name='PK_Loan'),
    )


class Grant(db.Model):
    """
    单次付款类
    """
    branchName = db.Column(db.String(20))
    loanId = db.Column(db.String(6))
    grantCount = db.Column(db.Integer)
    grantTime = db.Column(db.Date)
    grantMoney = db.Column(db.Float)
    __table_args__ = (
        db.PrimaryKeyConstraint('branchName', 'loanId', 'grantCount', name='PK_Grant'),
        db.ForeignKeyConstraint(['branchName', 'loanId'], ['Loan.branchName', 'Loan.loanId']),
    )


# ===== relationship ======

class OpenDepositAccount(db.Model):
    """
    开设储蓄账户
    """
    accountId = db.Column(db.String(20), db.ForeignKey('DepositAccount.id'), primary_key=True)
    clientId = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)


class OpenChequeAccount(db.Model):
    """
    开设支票账户
    """
    accountId = db.Column(db.String(20), db.ForeignKey('ChequeAccount.id'), primary_key=True)
    clientId = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)


class ServiceRelationship(db.Model):
    """
    业务关系，描述客户与银行的联系
    """
    branchName = db.Column(db.String(20), db.ForeignKey('Branch.branchName'), primary_key=True)
    clientId = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)


class OpenAccount(db.Model):
    """
    开户
    用户每开设一个支票账户或储蓄账户的同时也需要在此处创建一条记录。
    其用处为一个客户在一个支行只能开设一个储蓄账户和一个支票账户。
    该类的目的不在于查询，只在于实施该限制
    """
    branchName = db.Column(db.String(20), db.ForeignKey('Branch.branchName'), primary_key=True)
    id = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)
    depositAccountId = db.Column(db.String(20))
    chequeAccountId = db.Column(db.String(20))


class OwnLoan(db.Model):
    """
    拥有。客户拥有贷款的关系
    """
    branchName = db.Column(db.String(20), primary_key=True)
    loanId = db.Column(db.String(6), primary_key=True)
    clientId = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)
    __table_args__ = (
        db.ForeignKeyConstraint(['branchName', 'loanId'], ['Loan.branchName', 'Loan.loanId']),
    )


class Serve(db.Model):
    """
    服务。员工服务客户的关系。
    """
    clientId = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)
    staffId = db.Column(db.String(20), db.ForeignKey('Staff.id'), primary_key=True)
    ServiceType = db.Column(db.String(20))

