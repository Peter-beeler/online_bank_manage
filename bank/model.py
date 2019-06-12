# -*- coding: utf-8 -*-
from bank import db



class Branch(db.Model):
    """
    支行类
    """
    branchName = db.Column(db.String(20), primary_key=True)
    branchCity = db.Column(db.String(20))
    branchAsset = db.Column(db.Integer)

class Department(db.Model):
    """
    部门类
    """
    branchName = db.Column(db.String(20), primary_key=True)
    deptId = db.Column(db.Integer, primary_key=True)
    deptName = db.Column(db.String(20))
    deptType = db.Column(db.String(20))
    deptManagerID = db.Column(db.String(20))

class ChequeAccount(db.Model):
    """
    支票账户类
    """
    id = db.Column(db.String(20), primary_key=True)
    accountBalance = db.Column(db.Float)
    openTime = db.Column(db.DateTime)
    branchName = db.Column(db.String(20))
    visitTime = db.Column(db.DateTime)
    creditLimit = db.Column(db.Float)

class DepositAccount(db.Model):
    """
    储蓄账户类
    """
    id = db.Column(db.String(20), primary_key=True)
    accountBalance = db.Column(db.Float)
    openTime = db.Column(db.DateTime)
    branchName = db.Column(db.String(20))
    visitTime = db.Column(db.DateTime)
    interestRate = db.Column(db.Float)
    currencyType = db.Column(db.String(20))

class Staff(db.Model):
    """
    员工类
    """
    id = db.Column(db.String(20), unique=True)
    branchName = db.Column(db.Integer, db.ForeignKey('Branch.branchName'), index=True)
    deptId = db.Column(db.Integer)
    staffName = db.Column(db.String(20))
    staffPhone = db.Column(db.String(20))
    staffAddr = db.Column(db.String(40))
    startTime = db.Column(db.Date)

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
    branchName = db.Column(db.Integer, db.ForeignKey('Branch.branchName'), index=True)
    loanId = db.Column(db.String(6), unique=True)
    loanAmount = db.Column(db.Float)
    payNum = db.Column(db.Integer)

class Grant(db.Model):
    """
    单次付款类
    """
    branchName = db.Column(db.Integer, db.ForeignKey('branches.id'), index=True)
    loanId = db.Column(db.String(6), unique=True)
    grantCount = db.Column(db.Integer)
    grantTime = db.Column(db.Date)
    grantMoney = db.Column(db.Float)

# ===== relationship ======

class OpenDepositAccount(db.Model):
    """
    开设储蓄账户
    """
    accountId = db.Column(db.String(20), primary_key=True)
    id = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)

class OpenChequeAccount(db.Model):
    """
    开设支票账户
    """
    accountId = db.Column(db.String(20), primary_key=True)
    id = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)

class ServiceRelationship(db.Model):
    """
    业务关系，描述客户与银行的联系
    """
    branchName = db.Column(db.String(20), db.ForeignKey('Branch.branchName'), primary_key=True)
    id = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)

class OpenAcount(db.Model):
    """
    开户
    用户每开设一个支票账户或储蓄账户的同时也需要在此处创建一条记录。
    其用处为一个客户在一个支行只能开设一个储蓄账户和一个支票账户。
    该类的目的不在于查询，只在于实施该限制
    """
    branchName = db.Column(db.String(20), db.ForeignKey('Branch.branchName'), primary_key=True)
    id = db.Column(db.String(20), db.ForeignKey('Client.id'), primary_key=True)
    depositAccountId = db.Column(db.String(20),db.ForeignKey('DepositAccount.id'), primary_key=True)
    chequeAccountId = db.Column(db.String(20),db.ForeignKey('ChequeAccount.id'), primary_key=True)

class OwnLoan(db.Model):
    branchName = db.Column(db.String(20), db.ForeignKey('Branch.branchName'), primary_key=True)
    loanId = db.Column(db.String(6), db.ForeignKey('Branch.branchName'), unique=True)

class Serve(db.Model):
    """
    服务
    """
    clientId = db.Column(db.String(20), primary_key=True)
    staffId = db.Column(db.String(20), unique=True)
    ServiceType = db.Column(db.String(20))

