from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import utils
from app.models import CfgNotify
from app.main.forms import CfgNotifyForm
from . import main

logger = get_logger(__name__)
cfg = get_config()

# 通用列表查询
def common_list(DynamicModel, view):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    # 查询列表
    query = DynamicModel.select()
    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


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


# 支行查询
@main.route('/notifylist_bank', methods=['GET', 'POST'])
@login_required
def notifylist_bank():
    return common_list(CfgNotify, 'notifylist_bank.html')


# 支行管理
@main.route('/notifyedit_bank', methods=['GET', 'POST'])
@login_required
def notifyedit_bank():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit_bank.html')

# stuff
@main.route('/notifylist_stuff', methods=['GET', 'POST'])
@login_required
def notifylist_stuff():
    return common_list(CfgNotify, 'notifylist_stuff.html')


# stuff
@main.route('/notifyedit_stuff', methods=['GET', 'POST'])
@login_required
def notifyedit_stuff():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit_stuff.html')

# client
@main.route('/notifylist_client', methods=['GET', 'POST'])
@login_required
def notifylist_client():
    return common_list(CfgNotify, 'notifylist_client.html')

@main.route('/notifyedit_client', methods=['GET', 'POST'])
@login_required
def notifyedit_client():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit_client.html')

# account
@main.route('/notifylist_account', methods=['GET', 'POST'])
@login_required
def notifylist_account():
    return common_list(CfgNotify, 'notifylist_account.html')


@main.route('/notifyedit_account', methods=['GET', 'POST'])
@login_required
def notifyedit_account():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit_account.html')

# loan
@main.route('/notifylist_loans', methods=['GET', 'POST'])
@login_required
def notifylist_loans():
    return common_list(CfgNotify, 'notifylist_loans.html')

@main.route('/notifylist_loans2', methods=['GET', 'POST'])
@login_required
def notifylist_loans2():
    return common_list(CfgNotify, 'notifylist_loans.html')


@main.route('/notifyedit_loans', methods=['GET', 'POST'])
@login_required
def notifyedit_loans():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit_loans.html')

@main.route('/notifyedit_loans2', methods=['GET', 'POST'])
@login_required
def notifyedit_loans2():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit_loans2.html')


