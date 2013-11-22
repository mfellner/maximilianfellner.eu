# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, send_from_directory, current_app

from app.shared.models import JSendResponse
from app.http.auth import HTTPBasicAuth


shared_bp = Blueprint('shared_bp', __name__)
auth = HTTPBasicAuth()


@auth.unauthorized
def unauthorized():
    return JSendResponse.new_fail('unauthorized').jsonify(), 401


@shared_bp.route('/')
def get_root_index():
    return render_template('layout.html')


@shared_bp.route('/favicon.ico')
def get_favicon():
    return send_from_directory(os.path.join(current_app.static_folder, 'images'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@shared_bp.app_errorhandler(400)  # Bad Request (REST)
@shared_bp.app_errorhandler(401)  # Unauthorized (REST)
@shared_bp.app_errorhandler(405)  # Method Not Allowed (REST)
def handle_error(err):
    return JSendResponse.new_fail('%d: %s' % (err.code, err.description)).jsonify(), err.code


@shared_bp.app_errorhandler(403)  # Forbidden
def handle_403(err):
    return render_template('403.html', title='Forbidden'), 403


@shared_bp.app_errorhandler(404)  # Not Found
def handle_404(err):
    if hasattr(err, 'data') and err.data.get('rest', False):
        return JSendResponse.new_fail(str(err)).jsonify(), 404
    else:
        return render_template('404.html', title='Not Found'), 404


@shared_bp.app_errorhandler(500)  # Internal Server Error
def handle_500(err):
    if hasattr(err, 'data') and err.data.get('rest', False):
        return JSendResponse.new_error(str(err)).jsonify(), 500
    else:
        return render_template('500.html', title='Internal Server Error'), 500
