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

class BankClass(FlaskForm):
	bankName = StringField('支行名', validators=[Length(0, 20, message='长度不正确')])
	bankCity = StringField('城市', validators=[Length(0, 20, message='长度不正确')])
	bankAsset = IntegerField('资产', validators=[Length(0,20,message='长度不正确')])

class account(FlaskForm):
	ID = StringField('ID', validators=[Length(0,20,message='长度不正确')])
	branchName = StringField('所属支行', validators=[Length(0, 20, message='长度不正确')])
	acc_type = StringField('账户类型', anyof=['支票账户','储蓄账户'])
	balance = FloatField('余额', validators=[Length(0, 20, message='长度不正确')])
	openTime  = DateTimeField('开户时间')
	visitTime = DateTimeField('访问时间')
	creditLimit = FloatField('额度', validators=[Length(0, 20, message='长度不正确')])
	interestrate = FloatField('利率', validators=[Length(0, 20, message='长度不正确')])
	currencyType = StringField('货币类型', validators=[Length(0, 20, message='长度不正确')])

class client(FlaskForm):
	ID = StringField('ID', validators=[Length(0,20,message='长度不正确')])
	clientName = StringField('姓名', validators=[Length(0,20,message='长度不正确')])
	clientPhone = StringField('电话', validators=[Length(0,20,message='长度不正确')])
	clientAddr = StringField('地址', validators=[Length(0,40,message='长度不正确')])
	contactName = StringField('联系人姓名', validators=[Length(0,20,message='长度不正确')])
	contactPhone = StringField('联系人电话', validators=[Length(0,20,message='长度不正确')])
	contactEmail = StringField('联系人邮件', validators=[Length(0,40,message='长度不正确')])
	contactRelation = StringField('与本人关系', validators=[Length(0,10,message='长度不正确')])

class loans(FlaskForm):
	branchName = StringField('支行', validators=[Length(0,20,message='长度不正确')])
	loanId = StringField('ID', validators=[Length(0,6,message='长度不正确')])
	loanAmount = FloatField('数额', validators=[Length(0, 20, message='长度不正确')])
	payNum = IntegerField('逐次支付', validators=[Length(0,20,message='长度不正确')])


class grant(FlaskForm):
	branchName = StringField('支行', validators=[Length(0,20,message='长度不正确')])
	loanId = StringField('支行', validators=[Length(0,6,message='长度不正确')])
	grantCount = IntegerField('次数', validators=[Length(0,20,message='长度不正确')])
	grantTime = DateTimeField('支付时间')
	grantMoney = FloatField('金额', validators=[Length(0, 20, message='长度不正确')])





