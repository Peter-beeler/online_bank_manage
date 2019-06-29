from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import utils
from app.utils import flash_errors,form_to_model,model_to_form,query_to_list
from app.models import *
from app.main.forms import *
from . import main
import datetime
from peewee import *

from playhouse.shortcuts import dict_to_model, model_to_dict

logger = get_logger(__name__)
cfg = get_config()


# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# 首页


############2.根据支行的信息去查找所有对应支行的存储账户和支票账户
############2.根据支行的信息去查找所有的用户
############3.根据存储账户和支票账户的实践进行筛选
############4.统计出存储账户的总金额


def Select_All_Info(view):
    ############一个dict：
    ############dict的key为支行，映射到支行所属的一个列表 [[[业务金额，总用户数],[],[]],[[],[],[]]]
    ############对于每一个支行，第一个表示的是储蓄业务，第二个表示的是贷款业务

    All_Info_dict = []
    #*************1.select出所有的支行名字**********#
    branch_info = Branch.select()
    branch_name = []
    
    year_date   = datetime.datetime(2019,1,1)
    season_date = datetime.datetime(2019,3,1)
    month_date  = datetime.datetime(2019,6,1)
    print(year_date)
    print(season_date)
    print(month_date)

    for e in branch_info:
        branch_name.append( model_to_dict(e)['branchName'] )
    ####得到了所有的支行名称
    for e in branch_name:
        #**********根据每一个支行的名字进行选择***********#
        Info = []
        print(e)
        print(":AAAAAAAAAAAAAAAAAA")
        ######查找按年计算的储蓄金额
        deposit_query = OpenAccount.select( OpenAccount.depositAccountId ).distinct().where((OpenAccount.branchName == e) 
                                                and (OpenAccount.chequeAccountId == 'ffff' ))
        ######查找按季计算的储蓄金额

        ######查找按月计算的储蓄金额
        ######查找贷款
        branch_info = Branch.select().where(Branch.branchName == e)
        loan_query = Loan.select().distinct( Loan.loanId).where(Loan.branchName == branch_info )
        ########以上，得到了所有相关的存储账户和支票账户的ID,即属于该支行的存储/支票账户的ID
        #####

        #*****************************以下检索不同类型的账户涉及的金额数********************
        deposit_money_list=[]
        deposit_money_number = DepositAccount.select(
                                                fn.SUM(DepositAccount.accountBalance).alias("sum")
                                                ).where(
                                                    (DepositAccount.branchName == e) &
                                                    (DepositAccount.visitTime > year_date)
                                                ).execute()
        print("EEEEEEEEEEEEEEEEEEEE")
        for m in deposit_money_number:
            if m.sum !=None:
                deposit_money_list.append(m.sum)
            else:
                deposit_money_list.append(0.0)
            break

        deposit_money_number = DepositAccount.select(
                                                fn.SUM(DepositAccount.accountBalance).alias("sum")
                                                ).where(
                                                    (DepositAccount.branchName == e) &
                                                    (DepositAccount.visitTime > season_date)
                                                ).execute()
        print("EEEEEEEEEEEEEEEEEEEE")
        for m in deposit_money_number:
            if m.sum !=None:
                deposit_money_list.append(m.sum)
            else:
                deposit_money_list.append(0.0)
            break

        deposit_money_number = DepositAccount.select(
                                                fn.SUM(DepositAccount.accountBalance).alias("sum")
                                                ).where(
                                                    (DepositAccount.branchName == e) &
                                                    (DepositAccount.visitTime > month_date)
                                                ).execute()
        print("EEEEEEEEEEEEEEEEEEEE")
        for m in deposit_money_number:
            if m.sum !=None:
                deposit_money_list.append(m.sum)
            else:
                deposit_money_list.append(0.0)
            break
        '''
        这一部分实现了贷款总发放金额的统计
        '''
        loan_money_list = []
        loan_money_number = Grant1.select(fn.SUM(Grant1.grantMoney).alias("sum")).where(
                                                    (Grant1.branchName == e) &
                                                    (Grant1.grantTime > year_date)
                                                ).execute()
        for m in loan_money_number:
            if m.sum !=None:
                loan_money_list.append(m.sum)
            else:
                loan_money_list.append(0.0)
            break
        print("$$$$$$$$$$$$$$$$$$")
        print(loan_money_list)
        loan_money_number = Grant1.select(fn.SUM(Grant1.grantMoney).alias("sum")).where(
                                                    (Grant1.branchName == e) &
                                                    (Grant1.grantTime > season_date)
                                                ).execute()
        for m in loan_money_number:
            if m.sum !=None:
                loan_money_list.append(m.sum)
            else:
                loan_money_list.append(0.0)
            break
        print(loan_money_list)
        loan_money_number = Grant1.select(fn.SUM(Grant1.grantMoney).alias("sum")).where(
                                                    (Grant1.branchName == e) &
                                                    (Grant1.grantTime > month_date)
                                                ).execute()
        for m in loan_money_number:
            if m.sum !=None:
                loan_money_list.append(m.sum)
            else:
                loan_money_list.append(0.0)
            break
        print(loan_money_list)
        total_money = []
        total_money.append(deposit_money_list)
        total_money.append(loan_money_list)
        Info.append(total_money)
        #******************************以下检索不同类型的活跃用户***************************
        '''
        这一部分实现了储蓄用户的检索，join用于聚集
        '''
        deposit_user_list = []
        deposit_user_number  = OpenAccount.select(OpenAccount.id).distinct().join(
                                                DepositAccount,on=(
                                                    DepositAccount.id == OpenAccount.depositAccountId
                                                )).where(
                                                (OpenAccount.branchName == e) &
                                                (OpenAccount.chequeAccountId == 'ffff') &
                                                (DepositAccount.visitTime > year_date)
                                            ).count()   
        deposit_user_list.append(deposit_user_number)  
        deposit_user_number  = OpenAccount.select(OpenAccount.id).distinct().join(
                                                DepositAccount,on=(
                                                    DepositAccount.id == OpenAccount.depositAccountId
                                                )).where(
                                                (OpenAccount.branchName == e) &
                                                (OpenAccount.chequeAccountId == 'ffff') &
                                                (DepositAccount.visitTime > season_date)
                                            ).count()
        deposit_user_list.append(deposit_user_number)
        deposit_user_number  = OpenAccount.select(OpenAccount.id).distinct().join(
                                                DepositAccount,on=(
                                                    DepositAccount.id == OpenAccount.depositAccountId
                                                )).where(
                                                (OpenAccount.branchName == e) &
                                                (OpenAccount.chequeAccountId == 'ffff') &
                                                (DepositAccount.visitTime > month_date)
                                            ).count()
        deposit_user_list.append(deposit_user_number)
        '''
        虽然巨丑，但是实现了贷款用户的检索，首先join用于聚集，distinct用于查找不同的用户
        where语句中表示的是：当前支行的贷款情况+这一段时间之内拥有付款记录
        该类型的用户就可以被视为这一段时间的活跃用户数，表示银行与其产生了py关系
        '''   
        loan_user_list = []
        loan_user_number    = OwnLoan.select(OwnLoan.clientId).distinct().join(
                                                Grant1,on=(
                                                    (Grant1.loanId == OwnLoan.loanId) &
                                                    (Grant1.branchName == OwnLoan.branchName) 
                                                )).where(
                                                    (OwnLoan.branchName == e) &
                                                    (Grant1.grantTime > year_date)
                                            ).count()
        loan_user_list.append(loan_user_number)
        loan_user_number    = OwnLoan.select(OwnLoan.clientId).distinct().join(
                                                Grant1,on=(
                                                    (Grant1.loanId == OwnLoan.loanId) &
                                                    (Grant1.branchName == OwnLoan.branchName) 
                                                )).where(
                                                    (OwnLoan.branchName == e) &
                                                    (Grant1.grantTime > season_date)
                                            ).count()
        loan_user_list.append(loan_user_number)
        loan_user_number    = OwnLoan.select(OwnLoan.clientId).distinct().join(
                                                Grant1,on=(
                                                    (Grant1.loanId == OwnLoan.loanId) &
                                                    (Grant1.branchName == OwnLoan.branchName) 
                                                )).where(
                                                    (OwnLoan.branchName == e) &
                                                    (Grant1.grantTime > month_date)
                                            ).count()
        loan_user_list.append(loan_user_number)
        print("ALLLLLLLLLLLLLLL")
        print(deposit_user_number)
        print(loan_user_number)
        total_user = [deposit_user_list,loan_user_list]

        Info.append(total_user)
        print(Info)
        temp = {}
        temp['branchName'] = e
        temp["info"] = Info
        All_Info_dict.append(temp)
        print("ENDOFALOOP")
        print("")
    rel = {'content': All_Info_dict}
    print(rel)
    return render_template(view,form = rel,current_user = current_user)

@main.route('/index', methods=['GET'])
@login_required
def index():

    return render_template('index.html', current_user=current_user)


#========== 支行查询和相关管理==================
#++++++++++++++++++++++++++++这里是我复写的两个common方法，东西是共同的，但是主码的区别导致所有的方法必须被分开，不然没法用
def common_list_bank(DynamicModel,form,view):
    # 接收参数
    del_name = request.args.get('id')   ####从html代码中得到删除的相关信息
    model = DynamicModel()
    form_to_model(form, model)
    dct = model_to_dict(model) ####将model转化为dict，方便输出debug和输入
    name = dct['branchName']
    city = dct['branchCity']
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    print(dct)
    if del_name !=None:   
        try:
            account_count = OpenAccount.select().where( OpenAccount.branchName == del_name).count()
            print("SSSSSSSSSSS")
            staff_count    = Staff.select().where( Staff.branchName == del_name).count()
            print(account_count)
            print(staff_count)
            if account_count + staff_count == 0:
                print("dddddd")
                DynamicModel.get(DynamicModel.branchName == del_name).delete_instance()
                #Serve.get(DynamicModel.id == del_name).delete_instance()
                flash('删除成功')
            else:
                flash('该支行与账户/员工存在着绑定关系，无法删除')
        except:
            flash('删除失败')
    ####根据不同的现有数据进行查询，接下来的一些实现中可以放宽需求。
    if len(name) and len(city)  :
        query = DynamicModel.select().where((DynamicModel.branchName == name) & (DynamicModel.branchCity == city))
    elif len(name):
        query = DynamicModel.select().where(DynamicModel.branchName == name) 
    elif len(city):
        query = DynamicModel.select().where(DynamicModel.branchCity == city)
    else:
        query = DynamicModel.select()
    total_count = query.count()
    #####重新组织好查询结果
    list = []
    for e in query:
        list.append(model_to_dict(e))
    dict = {'content': list}
    print(dict)
    return render_template(view, form=dict,form_search = form,current_user=current_user)

def common_edit_bank(DynamicModel, form, view):
    # 查询是否在数据库中已经有了对应的条目
    if form.validate_on_submit():
        model = DynamicModel()
        form_to_model(form, model)
        dct = model_to_dict(model)
        name = dct['branchName']
        if DynamicModel.select().where(DynamicModel.branchName == name).count():  ###这一句话的含义是，通过查看对应的主码来判断是否存在对应的条目
            ####有了
            model.save()
            flash('修改成功')
        else:
            ###莫得
            DynamicModel.insert(dct).execute()
            flash('保存成功')
    else:
        flash_errors(form)
    return render_template(view, form=form, current_user=current_user)

#*************************以上需要在删除的时候，添加对应的关系查询项目，查看是否能够删除

#========== 客户查询和相关管理==================
def common_list_client(DynamicModel,form,view):
    # 接收参数
    del_id = request.args.get('id')   ####从html代码中得到删除的相关信息
    model = DynamicModel()
    form_to_model(form, model)
    dct = model_to_dict(model) ####将model转化为dict，方便输出debug和输入
    name = dct['clientName']
    this_id = dct['id']
    print(dct)
    if del_id !=None:   
        try:
            '''
            这里需要添加的是对于删除条件的审查
            '''
            #########同步添加
            #######寻找是否存在着关联的账户或者贷款
            print("PPPPPPPPPPPP")
            account_count = OpenAccount.select().where( OpenAccount.id == del_id).count()
            loan_count    = OwnLoan.select().where( OwnLoan.clientId == del_id).count()
            print("SSSSSSSSSS")
            if account_count + loan_count == 0:
                DynamicModel.get(DynamicModel.id == del_id).delete_instance()
                print("OOOOOOOOOOOOO")
                Serve.get(Serve.clientId == del_id ).delete_instance()
                flash('删除成功')
            else:
                flash('该用户与账户/贷款存在着绑定关系，无法删除')
        except:
            flash('删除失败')
    ####根据不同的现有数据进行查询，接下来的一些实现中可以放宽需求。
    if len(this_id) and len(name)  :
        query = DynamicModel.select().where((DynamicModel.id == this_id) & (DynamicModel.clientName == name))
    elif len(name):
        query = DynamicModel.select().where(DynamicModel.clientName == name) 
    elif len(this_id):
        query = DynamicModel.select().where(DynamicModel.id == this_id)
    else:
        query = DynamicModel.select()
    total_count = query.count()
    #####重新组织好查询结果
    list = []
    for e in query:
        list.append(model_to_dict(e))
    dict = {'content': list}
    print(dict)
    return render_template(view, form=dict,form_search = form,current_user=current_user)

def common_edit_client(DynamicModel, form, view):
    # 查询是否在数据库中已经有了对应的条目
    if form.validate_on_submit():
        model = DynamicModel()
        ##### 保存服务信息的相关字典
        print("AAAAAAAAAAAAAAAAAAAAA")
        print(request.form["Related_Staff"])
        Serve_dict = dict()
        Serve_dict['clientId'] = request.form['id']
        Serve_dict['staffId']  = request.form["Related_Staff"]
        Serve_dict['ServiceType'] = 'ServiceType'
        #######得到了相关负责人的信息
        form_to_model(form, model)
        dct = model_to_dict(model)
        print("AAAAAAAAAAAAAA")
        id = dct['id']
        if DynamicModel.select().where(DynamicModel.id == id).count():  ###这一句话的含义是，通过查看对应的主码来判断是否存在对应的条目
            ####有了
            model.save()
            flash('修改成功')
        else:
            ###莫得，需要在Serve表中也插入相关信息。
            DynamicModel.insert(dct).execute()
            flash('保存成功')
        if Serve.select().where(Serve.clientId == request.form["id"]).count() == 0:
            try:
                Serve.insert(Serve_dict).execute()
            except:
                flash('查无此员工')

        
    else:
        flash_errors(form)
    return render_template(view, form=form, current_user=current_user)
   

#========== 员工查询和相关管理==================
def common_list_staff(DynamicModel,form,view):
    # 接收参数
    del_id = request.args.get('id')   ####从html代码中得到删除的相关信息
    model = DynamicModel()
    form_to_model(form, model)
    dct = model_to_dict(model) ####将model转化为dict，方便输出debug和输入
    name = dct['staffName']
    branch = dct['branchName']
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    this_id = dct['id']
    print(dct)
    if del_id !=None:   
        try:
            #######寻找是否存在着关联的账户或者贷款
            print("QAW")
            print(del_id)
            Serve_count = Serve.select().where(Serve.staffId == del_id).count()
            print("QQQQQQQQQQQQQQQQQQ")
            if Serve_count == 0:
                DynamicModel.get(DynamicModel.id == del_id).delete_instance()
                flash('删除成功')
            else:
                flash('该用户与相关客户存在着服务绑定关系，无法删除')
        except:
            flash('删除失败')
    ####根据不同的现有数据进行查询，接下来的一些实现中可以放宽需求。
    if len(this_id) and len(name) and len(branch) :
        query = DynamicModel.select().where((DynamicModel.id == this_id) & (DynamicModel.staffName == name) & (DynamicModel.branchName == branch))
    elif len(name):
        query = DynamicModel.select().where(DynamicModel.staffName == name) 
    elif len(this_id):
        query = DynamicModel.select().where(DynamicModel.id == this_id)
    elif len(branch):
        query = DynamicModel.select().where(DynamicModel.branchName == branch)
    else:
        query = DynamicModel.select()
    total_count = query.count()
    #####重新组织好查询结果
    list = []
    for e in query:
        list.append(model_to_dict(e))
    dict = {'content': list}
    print(dict)
    return render_template(view, form=dict,form_search = form,current_user=current_user)

def common_edit_staff(DynamicModel, form, view):
    # 查询是否在数据库中已经有了对应的条目
    if form.validate_on_submit():
        model = DynamicModel()
        form_to_model(form, model)
        dct = model_to_dict(model)
        print("AAAAAAAAAAAAAA")
        print(dct)
        id = dct['id']
        if DynamicModel.select().where(DynamicModel.id == id).count():  ###这一句话的含义是，通过查看对应的主码来判断是否存在对应的条目
            ####有了
            model.save()
            flash('修改成功')
        else:
            ###莫得
            DynamicModel.insert(dct).execute()
            flash('保存成功')
    else:
        flash_errors(form)
    return render_template(view, form=form, current_user=current_user)

#========== 账户查询和相关管理==================
def common_list_account(DynamicModel,form,view):
    # 接收参数
    del_id = request.args.get('id')   ####从html代码中得到删除的相关信息
    model = DynamicModel()
    form_to_model(form, model)
    dct = model_to_dict(model) ####将model转化为dict，方便输出debug和输入
    this_id = dct['id']
    branchname = dct['branchName']
    if branchname == None:
        branchname = ''
    if this_id == None:
        this_id = ''
    print(len(this_id))
    try:
        branchname = dct['branchName']['branchName']
    except: 
        branchname = ''
    print(len(branchname))
    print(dct)
    if del_id !=None:   
        try:
            print("EEEEEEEEEEEEEE")
            print(del_id)
            ######找出所有的和当前要删除账户id相关联的账户的关系，并且挨个删除
            query = OpenAccount.select().where((OpenAccount.depositAccountId == del_id) | (OpenAccount.chequeAccountId == del_id) )
            print("AAAAAAAAAAAAA")
            for e in query:
                e.delete_instance()
            DynamicModel.get(DynamicModel.id == del_id).delete_instance()    
            flash('删除成功')
        except:
            flash('删除失败')
    ####根据不同的现有数据进行查询，接下来的一些实现中可以放宽需求。
    #branch = Branch.select().where(Branch.branchName == branchname)
    if len(this_id) and len(branchname) :
        query = DynamicModel.select().where((DynamicModel.id == this_id)  & (DynamicModel.branchName == branchname))
    elif len(this_id):
        query = DynamicModel.select().where(DynamicModel.id == this_id)
    elif len(branchname):
        query = DynamicModel.select().where(DynamicModel.branchName == branchname)
    else:
        query = DynamicModel.select()
    total_count = query.count()
    #####重新组织好查询结果
    list = []
    for e in query:
        temp = model_to_dict(e)
        temp['branchName'] = temp['branchName']['branchName']
        list.append(temp)
    dict = {'content': list}
    print(dict)
    return render_template(view, form=dict,form_search = form,current_user=current_user)

def common_edit_account(DynamicModel, form, view):
    # 查询是否在数据库中已经有了对应的条目
    if form.validate_on_submit():
        model = DynamicModel()
        ##### 保存账户关联信息的相关字典
        A_dict = dict()
        A_dict['branchName'] = form.data['branchName']
        A_dict['id']  = form.data['Related_Customer']
        print("AAAAAAAAAAAAAAAAK")
        print (form.data['branchName'])
        credit = 1
        try:
            print (form.data['creditLimit'])
        except:
            credit = 0
        print("BBBBBBBBB")
        if  credit == 0:
            A_dict['depositAccountId'] = form.data['id']
            A_dict['chequeAccountId']  = 'ffff'
        else:
            A_dict['depositAccountId'] = 'ffff'
            A_dict['chequeAccountId']  = form.data['id']

        form_to_model(form, model)
        dct = model_to_dict(model)
        dct['branchName'] = dct['branchName']['branchName']
        id = dct['id']        
        #**********************接下来，根据相关信息增加联系，联系只可能添加或者删除，不可能修改。********************
        #########首先查看该账户关系是否已经存在，如果已经存在，直接跳过并开始修改
        #########
        #######如果说查找该账户和该账户所有者，没有相关联系，那么就是还没建立起相关联系
        query = OpenAccount.select().where((OpenAccount.branchName == form.data["branchName"]) 
                                            & (OpenAccount.id == form.data["Related_Customer"]) )
        ######先查一下该客户在该行有没有存储/支票账户
        flag_cheque = 1
        flag_deposit = 1
        for e in query:
            temp = model_to_dict(e)
            if temp['chequeAccountId'] != 'ffff':   #####此时已经有了一个支票账户了
                print("有支票账户了！")
                flag_cheque = 0
            if temp['depositAccountId'] != 'ffff':  #####此时已经有了一个存储账户了
                print("有存储账户了！")
                flag_deposit = 0
        flag = 0
        no_user = 0
        print(credit)
        print(flag_deposit)
        if (flag_deposit and  credit == 0 ) or (flag_cheque and  credit):  
            ##表明此时可能还能插对应的账户
            try:
                flag = 1    #####表明此时可以插入新的账户
                OpenAccount.insert(A_dict).execute()
            except:
                no_user = 1
                flash("无法插入账户，相关用户不存在于银行记录中！")
        else:#########此时表明不可以继续插账户了
            flash("该用户不可继续增加账户")
        if DynamicModel.select().where(DynamicModel.id == id).count():  ###这一句话的含义是，通过查看对应的主码来判断是否存在对应的条目
            ####账户已经存在，则可以修改
            model.save()
            flash('修改成功')
        else:####如果说该账户尚未存在，且与该账户关联的用户已经达到了上限
            ###莫得
            if flag == 1 and no_user == 0:
                print(dct)
                DynamicModel.insert(dct).execute()
                flash('账户保存成功')
    else:
        flash_errors(form)
    return render_template(view, form_search=form, current_user=current_user)

#********************在插入账户的时候，需要添加用户和账户之间的关系，同时需要检查是否已经有了此类账户的约束
#********************在删除账户的时候，需要同步删除该账户涉及到的所有的关系中的信息


#========== 贷款查询和相关管理==================
#++++++++++++++++++++++++++++这里是我复写的两个common方法，东西是共同的，但是主码的区别导致所有的方法必须被分开，不然没法用
def common_list_loan(DynamicModel,form,view):
    # 接收参数
    del_id = request.args.get('id')   ####从html代码中得到删除的相关信息
    model = DynamicModel()
    form_to_model(form, model)
    dct = model_to_dict(model) ####将model转化为dict，方便输出debug和输入
    this_id = dct['loanId']
    try:
        branchname = dct['branchName']['branchName']
    except:
        branchname = ''
    print(dct)
    if del_id !=None:   
        try:
            ####首先需要检查当前的贷款的发放次数是否已经到达了上限，如果发放次数大于零且小于上界，则证明还处于发放中。
            loan_info = Loan.get(Loan.loanId == del_id)   #####这个是当前的贷款信息
            loan_dict = model_to_dict(loan_info)
            total_num  = loan_dict['payNum']
            actual_num = Grant1.select().where(Grant1.loanId == del_id).count()
            print(actual_num)
            if actual_num == 0 or total_num <= actual_num:
                DynamicModel.get(DynamicModel.loanId == del_id).delete_instance()
                flash('删除成功')
            else:
                flash("贷款仍然在发放中，不可删除当前贷款信息！")
        except:
            flash('删除失败')
    ####根据不同的现有数据进行查询，接下来的一些实现中可以放宽需求。
    branch = Branch.select().where(Branch.branchName == branchname)
    if len(this_id) and len(branch) :
        query = DynamicModel.select().where((DynamicModel.loanId == this_id)  & (DynamicModel.branchName == branch))
    elif len(this_id):
        query = DynamicModel.select().where(DynamicModel.loanId == this_id)
    elif len(branch):
        query = DynamicModel.select().where(DynamicModel.branchName == branch)
    else:
        query = DynamicModel.select()
    total_count = query.count()
    #####重新组织好查询结果
    list = []
    for e in query:
        temp = model_to_dict(e)
        temp['branchName'] = temp['branchName']['branchName']
        #####查询所有贷款的支付情况
        temp_id = temp['loanId']
        this_actual_num = Grant1.select().where(Grant1.loanId == temp_id).count()
        this_total_num  = temp['payNum']
        if this_total_num == None:
            this_total_num = 0
        if this_actual_num == 0:
            state = '未支付'
        elif this_actual_num >=this_total_num:
            state = '支付完成'
        else:
            state = '支付中'
        temp['state'] = state
    ########以上为查询当前的贷款的状态
        list.append(temp)
    dict = {'content': list}
    return render_template(view, form=dict,form_search = form,current_user=current_user)

def common_edit_loan(DynamicModel, form, view):
    # 查询是否在数据库中已经有了对应的条目
    if form.validate_on_submit():
        model = DynamicModel()

        Loan_dict = dict()
        Loan_dict['branchName'] = request.form['branchName']
        Loan_dict['loanId']  = request.form["loanId"]
        Loan_dict['clientId'] = request.form["Related_Customer"]

        form_to_model(form, model)
        dct = model_to_dict(model)
        dct['branchName'] = dct['branchName']['branchName']
        id = dct['loanId']
        no_user = 0
        if OwnLoan.select().where((OwnLoan.clientId == request.form['Related_Customer']) & (OwnLoan.loanId == request.form['loanId']) ).count() == 0:
            ####如果说此时关系表中，用户和贷款的关系还没有被建立起来
            try:
                OwnLoan.insert(Loan_dict).execute()
                flash("插入贷款新拥有者成功！")
            except:
                flash('查无此用户！,不可插入新贷款拥有者！')
                no_user = 1
        if DynamicModel.select().where(DynamicModel.loanId == id).count() :  
            ###这一句话的含义是，通过查看对应的主码来判断是否存在对应的条目
            ####有了
            flash('不可修改已有贷款信息！')
        else:
            ###莫得
            if no_user == 0:
                print(dct)
                DynamicModel.insert(dct).execute()
                flash('保存成功')
    else:
        flash_errors(form)
    return render_template(view, form_search=form, current_user=current_user)

def common_list_grant(DynamicModel,form,view):
    # 接收参数
    del_id = request.args.get('id')   ####从html代码中得到删除的相关信息
    del_count = request.args.get('count')
    del_branch =request.args.get('bname') 
    print(del_id)
    print(del_count)
    print(del_branch)
    print("FFFFFFFFFFFFFF")
    model = DynamicModel()
    form_to_model(form, model)
    dct = model_to_dict(model) ####将model转化为dict，方便输出debug和输入
    this_id = dct['loanId']
    branch = dct['branchName']
    print(dct)
    if del_id !=None and del_count !=None:   
        try:
            
            print("FFFFFFFF")
            models = DynamicModel.get( (DynamicModel.loanId == del_id)
                                    & (DynamicModel.grantCount == del_count)
                                    & (DynamicModel.branchName == del_branch)).delete_instance()
            counter = DynamicModel.select().where( (DynamicModel.loanId == del_id)
                                    & (DynamicModel.grantCount > del_count)
                                    & (DynamicModel.branchName == del_branch)).count()
            print(counter)
            up = DynamicModel.update(grantCount = DynamicModel.grantCount-1).where( (DynamicModel.loanId == del_id)
                                    & (DynamicModel.grantCount > del_count)
                                    & (DynamicModel.branchName == del_branch))
            up.execute()
            
            flash('删除成功')
        except:
            flash('删除失败')
    ####根据不同的现有数据进行查询，接下来的一些实现中可以放宽需求。
    if len(this_id) and len(branch) :
        query = DynamicModel.select().where((DynamicModel.loanId == this_id)  & (DynamicModel.branchName == branch))
    elif len(this_id):
        query = DynamicModel.select().where(DynamicModel.loanId == this_id)
    elif len(branch):
        query = DynamicModel.select().where(DynamicModel.branchName == branch)
    else:
        query = DynamicModel.select()
    total_count = query.count()
    #####重新组织好查询结果
    list = []
    for e in query:
        temp = model_to_dict(e)
        list.append(temp)
    dict = {'content': list}
    print(dict)
    return render_template(view, form=dict,form_search = form,current_user=current_user)

def common_edit_grant(DynamicModel, form, view):
    # 查询是否在数据库中已经有了对应的条目
    if form.validate_on_submit():
        model = DynamicModel()
        form_to_model(form, model)
        dct = model_to_dict(model)
        loan_id = dct['loanId']
        branch = dct['branchName']
        all_count = dct['grantCount']
        print(dct)
        print(all_count)
        print(loan_id)
        select_count = DynamicModel.select().where( (DynamicModel.loanId      == loan_id )
                                                &   (DynamicModel.branchName  == branch)
                                                &   (DynamicModel.grantCount  <= all_count)).count()
        #######查找所有的grantCount小于当前值的select
        print(select_count)
        if select_count == all_count :  
            ###这一句话的含义是，如果查到的数据是完整的，如输入1，查出了0,表示小于等于1的没有，可以修改
            ####有了
            print("ASDF")
            ########当前发放的总额度数
            actual_money = 0
            actual_record = DynamicModel.select(DynamicModel.grantMoney).where(DynamicModel.loanId == loan_id)
            for k in actual_record:
                actual_money += model_to_dict(k)['grantMoney']
            print(actual_money)
            #######实际应当发放的总额度数
            total_money = Loan.select().where(Loan.loanId == loan_id)
            print(total_money.count())
            for e in total_money:
                money_dict = model_to_dict(e)
                branch_name = money_dict['branchName']['branchName'] 
                if branch_name == branch:
                    total_money = money_dict['loanAmount']     
            try:       
                if total_money < actual_money + dct['grantMoney']:
                    flash("修改失败，发放贷款的数额超过了可以发放的总额")
                else:
                    model.save()
                    flash('修改成功')
            except:
                flash("无法修改，无此支行或ID！")
        elif select_count == all_count-1:  ######如果是顺序的
            ###莫得

            #######当前发放的总额度
            actual_money = 0
            actual_record = DynamicModel.select(DynamicModel.grantMoney).where(DynamicModel.loanId == loan_id)
            for k in actual_record:
                actual_money += model_to_dict(k)['grantMoney']
            print(actual_money)
            ######实际应当发放的总金额
            total_money = Loan.select().where(Loan.loanId == loan_id)
            print(total_money.count())
            for e in total_money:
                money_dict = model_to_dict(e)
                branch_name = money_dict['branchName']['branchName'] 
                if branch_name == branch:
                    total_money = money_dict['loanAmount']            
            if total_money < actual_money + dct['grantMoney']:
                flash("插入失败，发放贷款的数额超过了可以发放的总额")
            else:
                DynamicModel.insert(dct).execute()
                flash('保存成功')
        else:
            flash("未按序发放贷款")
    else:
        flash_errors(form)
    return render_template(view, form_search=form, current_user=current_user)


#*********************在插入贷款的时候，需要添加到用户和


@main.route('/notifylist_bank', methods=['GET', 'POST'])
@login_required
def notifylist_bank():
    return common_list_bank(Branch, Bank(), 'notifylist_bank.html')
    #######################################################对于html页面，删除与分页相关的东西就可以了，对比一下能看出来
# 支行管理

@main.route('/notifyedit_bank', methods=['GET', 'POST'])
@login_required
def notifyedit_bank():
    return common_edit_bank(Branch, Bank(), 'notifyedit_bank.html')


# ============员工管理部分============
# stuff
@main.route('/notifylist_stuff', methods=['GET', 'POST'])
@login_required
def notifylist_stuff():
    return common_list_staff(Staff,staff(),'notifylist_stuff.html')


# stuff
@main.route('/notifyedit_stuff', methods=['GET', 'POST'])
@login_required
def notifyedit_stuff():
    return common_edit_staff(Staff,staff(), 'notifyedit_stuff.html')



# ==================用户管理部分=========
@main.route('/notifylist_client', methods=['GET', 'POST'])
@login_required
def notifylist_client():
    return common_list_client(Client, client(), 'notifylist_client.html')

@main.route('/notifyedit_client', methods=['GET', 'POST'])
@login_required
def notifyedit_client():
    return common_edit_client(Client, client(), 'notifyedit_client.html')


#==================账户管理部分================
@main.route('/notifylist_account', methods=['GET', 'POST'])
@login_required
def notifylist_account():
    return common_list_account(ChequeAccount,account(), 'notifylist_account.html')


@main.route('/notifyedit_account', methods=['GET', 'POST'])
@login_required
def notifyedit_account():
    return common_edit_account(ChequeAccount, account(), 'notifyedit_account.html')

@main.route('/notifylist_account2', methods=['GET', 'POST'])
@login_required
def notifylist_account2():
    return common_list_account(DepositAccount,account2(), 'notifylist_account2.html')


@main.route('/notifyedit_account2', methods=['GET', 'POST'])
@login_required
def notifyedit_account2():
    return common_edit_account(DepositAccount, account2(), 'notifyedit_account2.html')

#====================贷款管理===================
@main.route('/notifylist_loans', methods=['GET', 'POST'])
@login_required
def notifylist_loans():
    return common_list_loan(Loan,loans(), 'notifylist_loans.html')

@main.route('/notifylist_loans2', methods=['GET', 'POST'])
@login_required
def notifylist_loans2():
    return common_list_grant(Grant1, grant(),'notifylist_loans2.html')


@main.route('/notifyedit_loans', methods=['GET', 'POST'])
@login_required
def notifyedit_loans():
    return common_edit_loan(Loan, loans(), 'notifyedit_loans.html')

@main.route('/notifyedit_loans2', methods=['GET', 'POST'])
@login_required
def notifyedit_loans2():
    return common_edit_grant(Grant1, grant(), 'notifyedit_loans2.html')

@main.route('/notifyedit_info', methods=['GET', 'POST'])
@login_required
def notifylist_info():
    return Select_All_Info('notifylist_info.html')
