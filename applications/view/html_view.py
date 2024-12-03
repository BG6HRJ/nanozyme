from flask import Blueprint, render_template

bp = Blueprint('html_view', __name__, url_prefix='/')


@bp.get('/')
def main():
    return render_template('hello.html')


@bp.route('/base')
def base():
    return render_template('base.html')


@bp.route('/advanced')
def advanced():
    return render_template('advanced.html')


@bp.route('/database')
def database():
    return render_template('database.html')


@bp.route('/offer_a_sample')
def offer_a_sample():
    return render_template('offer_a_sample.html')


@bp.route('/details_page')
def details_page():
    return render_template('details_page.html')


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/compare_predictions')
def compare_predictions():
    return render_template('compare_predictions.html')


@bp.route('/gpt')
def gpt():
    return render_template('gpt.html')


@bp.route('/about')
def about():
    return render_template('about.html')
