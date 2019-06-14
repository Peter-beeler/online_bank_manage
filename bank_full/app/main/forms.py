from flask_wtf import FlaskForm
from wtforms import * 
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class CfgNotifyForm(FlaskForm):
	check_order = StringField('排序', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
	notify_type = SelectField('通知类型', choices=[('MAIL', '邮件通知'), ('SMS', '短信通知')],validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
	notify_name = StringField('通知人姓名', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
	notify_number = StringField('通知号码', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
	status = BooleanField('生效标识', default=True)
	submit = SubmitField('提交')

class Bank(FlaskForm):
	branchName = StringField('支行名', validators=[Length(0, 20, message='长度不正确')],default = "gonghang")
	branchCity = StringField('城市', validators=[Length(0, 20, message='长度不正确')],default = "beijing")
	branchAsset = IntegerField('资产')
	submit = SubmitField('提交')

class account(FlaskForm):
	id = StringField('ID', validators=[Length(0,20,message='长度不正确')],default = '0000')
	branchName = StringField('所属支行', validators=[Length(0, 20, message='长度不正确')],default = 'a')
	accountBalance = FloatField('余额')
	openTime  = DateField('开户时间')
	visitTime = DateField('访问时间')
	creditLimit = FloatField('额度')
	submit = SubmitField('提交')

class account2(FlaskForm):
	id = StringField('ID', validators=[Length(0,20,message='长度不正确')],default = '0000')
	branchName = StringField('所属支行', validators=[Length(0, 20, message='长度不正确')],default = 'a')
	accountBalance = FloatField('余额')
	openTime  = DateField('开户时间')
	visitTime = DateField('访问时间')
	interestRate = FloatField('利率')
	currencyType = StringField('货币类型', validators=[Length(0, 20, message='长度不正确')])
	submit = SubmitField('提交')

class client(FlaskForm):
	id = StringField('ID', validators=[Length(0,20,message='长度不正确')],default = '1111')
	clientName = StringField('姓名', validators=[Length(0,20,message='长度不正确')],default = "null")
	clientPhone = StringField('电话', validators=[Length(0,20,message='长度不正确')])
	clientAddr = StringField('地址', validators=[Length(0,40,message='长度不正确')])
	contactName = StringField('联系人姓名', validators=[Length(0,20,message='长度不正确')])
	contactPhone = StringField('联系人电话', validators=[Length(0,20,message='长度不正确')])
	contactEmail = StringField('联系人邮件', validators=[Length(0,40,message='长度不正确')])
	contactRelation = StringField('与本人关系', validators=[Length(0,10,message='长度不正确')])
	submit = SubmitField('提交')

class loans(FlaskForm):
	branchName = StringField('支行', validators=[Length(0,20,message='长度不正确')],default = 'a')
	loanId = StringField('ID', validators=[Length(0,6,message='长度不正确')],default = '0000')
	loanAmount = FloatField('数额')
	payNum = IntegerField('逐次支付')
	submit = SubmitField('提交')


class grant(FlaskForm):
	branchName = StringField('支行', validators=[Length(0,20,message='长度不正确')],default = 'a')
	loanId = StringField('支行', validators=[Length(0,6,message='长度不正确')],default = '1111')
	grantCount = IntegerField('次数')
	grantTime = DateField('支付时间')
	grantMoney = FloatField('金额')
	submit = SubmitField('提交')

class staff(FlaskForm):
	id = StringField('ID', validators=[Length(0,20,message='长度不正确')],default = '0000')
	branchName = StringField('支行', validators=[Length(0,20,message='长度不正确')],default = 'a')
	deptId = IntegerField('部门')
	staffName = StringField('姓名', validators=[Length(0,20,message='长度不正确')],default = 'peter')
	staffPhone = StringField('电话', validators=[Length(0,20,message='长度不正确')])
	staffAddr = StringField('地址', validators=[Length(0,20,message='长度不正确')])
	startDate = DateField('支付时间')
	submit = SubmitField('提交')



