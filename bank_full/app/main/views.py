from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import utils
from app.utils import flash_errors,form_to_model,model_to_form,query_to_list
from app.models import *
from app.main.forms import *
from . import main

from playhouse.shortcuts import dict_to_model, model_to_dict

logger = get_logger(__name__)
cfg = get_config()


# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# 首页
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
    print(dct)
    if del_name !=None:   ####严重问题：由于我没有看懂html代码，因此这里每次执行删除操作后似乎没法继续查找，只有退出再进来才行
        ######################总之就是显示的非常混乱就对了
        try:
            account_count = OpenAccount.select().where( OpenAccount.branchName == del_id).count()
            staff_count    = Staff.select().where( Staff.branchName == del_id).count()
            if account_count + staff_count:
                DynamicModel.get(DynamicModel.id == del_id).delete_instance()
                Serve.get(DynamicModel.id == del_id ).delete_instance()
                flash('删除成功')
            else:
                flash('该支行与账户/员工存在着绑定关系，无法删除')
            flash('删除成功')
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
            account_count = OpenAccount.select().where( OpenAccount.id == del_id).count()
            loan_count    = OwnLoan.select().where( OwnLoan.clientId == del_id).count()
            if account_count + loan_count:
                DynamicModel.get(DynamicModel.id == del_id).delete_instance()
                Serve.get(DynamicModel.id == del_id ).delete_instance()
                flash('删除成功')
            else:
                flash('该用户与账户/贷款存在着绑定关系，无法删除')
            flash('删除成功')
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
    this_id = dct['id']
    print(dct)
    if del_id !=None:   
        try:
            #######寻找是否存在着关联的账户或者贷款
            Serve_count = Serve.select().where( Serve.staffId == del_id).count()
            #loan_count    = OwnLoan.select().where( OwnLoan.clientId == del_id)
            if Serve_count:
                DynamicModel.get(DynamicModel.id == del_id).delete_instance()
                flash('删除成功')
            else:
                flash('该用户与相关服务客户存在着绑定关系，无法删除')
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
    dct['branchName'] = dct['branchName']['branchName']
    print(dct)
    if del_id !=None:   
        try:
            DynamicModel.get(DynamicModel.id == del_id).delete_instance()
            ######找出所有的和当前要删除账户id相关联的账户的关系，并且挨个删除
            query = OpenAccount.select().where((OpenAccount.depositAccount == del_id) or (OpenAccount.chequeAccount == del_id) )
            for e in query:
                e.delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')
    ####根据不同的现有数据进行查询，接下来的一些实现中可以放宽需求。
    branch = Branch.select().where(Branch.branchName == branchname)
    if len(this_id) and len(branch) :
        query = DynamicModel.select().where((DynamicModel.id == this_id)  & (DynamicModel.branchName == branch))
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
        print(credit)
        print(flag_deposit)
        if (flag_deposit and  credit == 0 ) or (flag_cheque and  credit):  
            ##表明此时可能还能插对应的账户
            try:
                flag = 1    #####表明此时可以插入新的账户
                OpenAccount.insert(A_dict).execute()
            except:
                flash("？？？？")
        else:#########此时表明不可以继续插账户了
            flash("该用户不可继续增加账户")
        if DynamicModel.select().where(DynamicModel.id == id).count():  ###这一句话的含义是，通过查看对应的主码来判断是否存在对应的条目
            ####账户已经存在，则可以修改
            model.save()
            flash('修改成功')
        else:####如果说该账户尚未存在，且与该账户关联的用户已经达到了上限
            ###莫得
            if flag == 1:
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
    branchname = dct['branchName']['branchName']
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
        if DynamicModel.select().where(DynamicModel.loanId == id).count():  ###这一句话的含义是，通过查看对应的主码来判断是否存在对应的条目
            ####有了
            flash('不可修改已有贷款信息！')
        else:
            ###莫得
            print(dct)
            DynamicModel.insert(dct).execute()
            flash('保存成功')
    else:
        flash_errors(form)
    if OwnLoan.select().where( (OwnLoan.clientId == request.form["Related_Customer"])
                            and (OwnLoan.loanId == request.form['loanId']) ).count() == 0:
        ####如果说此时关系表中，用户和贷款的关系还没有被建立起来
        try:
            OwnLoan.insert(Loan_dict).execute()
        except:
            flash('查无此员工')
    return render_template(view, form_search=form, current_user=current_user)

def common_list_grant(DynamicModel,form,view):
    # 接收参数
    del_id = request.args.get('id')   ####从html代码中得到删除的相关信息
    model = DynamicModel()
    form_to_model(form, model)
    dct = model_to_dict(model) ####将model转化为dict，方便输出debug和输入
    this_id = dct['loanId']
    branch = dct['branchName']
    print(dct)
    if del_id !=None:   
        try:
            DynamicModel.get(DynamicModel.loanId == del_id).delete_instance()
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
        id = dct['loanId']
        print(dct)
        if DynamicModel.select().where(DynamicModel.loanId == id).count():  ###这一句话的含义是，通过查看对应的主码来判断是否存在对应的条目
            ####有了
            model.save()
            flash('修改成功')
        else:
            ###莫得
            print(dct)
            DynamicModel.insert(dct).execute()
            flash('保存成功')
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


