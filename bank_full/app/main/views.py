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
            DynamicModel.get(DynamicModel.branchName == del_name).delete_instance()
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


#========== 客户查询和相关管理==================
#++++++++++++++++++++++++++++这里是我复写的两个common方法，东西是共同的，但是主码的区别导致所有的方法必须被分开，不然没法用
def common_list_client(DynamicModel,form,view):
    # 接收参数
    del_id = request.args.get('id')   ####从html代码中得到删除的相关信息
    model = DynamicModel()
    form_to_model(form, model)
    dct = model_to_dict(model) ####将model转化为dict，方便输出debug和输入
    name = dct['clientName']
    this_id = dct['id']
    print(dct)
    if del_id !=None:   ####严重问题：由于我没有看懂html代码，因此这里每次执行删除操作后似乎没法继续查找，只有退出再进来才行
        ######################总之就是显示的非常混乱就对了
        try:
            DynamicModel.get(DynamicModel.id == del_id).delete_instance()
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
        form_to_model(form, model)
        dct = model_to_dict(model)
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
   

#========== 员工查询和相关管理==================
#++++++++++++++++++++++++++++这里是我复写的两个common方法，东西是共同的，但是主码的区别导致所有的方法必须被分开，不然没法用
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
    if del_id !=None:   ####严重问题：由于我没有看懂html代码，因此这里每次执行删除操作后似乎没法继续查找，只有退出再进来才行
        ######################总之就是显示的非常混乱就对了
        try:
            DynamicModel.get(DynamicModel.id == del_id).delete_instance()
            flash('删除成功')
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
#++++++++++++++++++++++++++++这里是我复写的两个common方法，东西是共同的，但是主码的区别导致所有的方法必须被分开，不然没法用
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
    if del_id !=None:   ####严重问题：由于我没有看懂html代码，因此这里每次执行删除操作后似乎没法继续查找，只有退出再进来才行
        ######################总之就是显示的非常混乱就对了
        try:
            DynamicModel.get(DynamicModel.id == del_id).delete_instance()
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
        form_to_model(form, model)
        dct = model_to_dict(model)
        dct['branchName'] = dct['branchName']['branchName']
        id = dct['id']
        if DynamicModel.select().where(DynamicModel.id == id).count():  ###这一句话的含义是，通过查看对应的主码来判断是否存在对应的条目
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
    if del_id !=None:   ####严重问题：由于我没有看懂html代码，因此这里每次执行删除操作后似乎没法继续查找，只有退出再进来才行
        ######################总之就是显示的非常混乱就对了
        try:
            DynamicModel.get(DynamicModel.loanId == del_id).delete_instance()
            flash('删除成功')
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
        list.append(temp)
    dict = {'content': list}
    print(dict)
    return render_template(view, form=dict,form_search = form,current_user=current_user)

def common_edit_loan(DynamicModel, form, view):
    # 查询是否在数据库中已经有了对应的条目
    if form.validate_on_submit():
        model = DynamicModel()
        form_to_model(form, model)
        dct = model_to_dict(model)
        dct['branchName'] = dct['branchName']['branchName']
        id = dct['loanId']
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

def common_list_grant(DynamicModel,form,view):
    # 接收参数
    del_id = request.args.get('id')   ####从html代码中得到删除的相关信息
    model = DynamicModel()
    form_to_model(form, model)
    dct = model_to_dict(model) ####将model转化为dict，方便输出debug和输入
    this_id = dct['loanId']
    branch = dct['branchName']
    print(dct)
    if del_id !=None:   ####严重问题：由于我没有看懂html代码，因此这里每次执行删除操作后似乎没法继续查找，只有退出再进来才行
        ######################总之就是显示的非常混乱就对了
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


