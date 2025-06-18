from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.content import Content, ClientLogo
from flask_cors import cross_origin
import os

content_bp = Blueprint('content', __name__)

@content_bp.route('/content', methods=['GET'])
@cross_origin()
def get_all_content():
    """جلب جميع المحتوى"""
    content = Content.query.all()
    return jsonify([item.to_dict() for item in content])

@content_bp.route('/content/<section>', methods=['GET'])
@cross_origin()
def get_content_by_section(section):
    """جلب المحتوى حسب القسم"""
    content = Content.query.filter_by(section=section).all()
    return jsonify([item.to_dict() for item in content])

@content_bp.route('/content', methods=['POST'])
@cross_origin()
def create_content():
    """إنشاء محتوى جديد"""
    data = request.get_json()
    
    content = Content(
        section=data['section'],
        key=data['key'],
        value=data['value'],
        content_type=data.get('content_type', 'text')
    )
    
    db.session.add(content)
    db.session.commit()
    
    return jsonify(content.to_dict()), 201

@content_bp.route('/content/<int:content_id>', methods=['PUT'])
@cross_origin()
def update_content(content_id):
    """تحديث المحتوى"""
    content = Content.query.get_or_404(content_id)
    data = request.get_json()
    
    content.section = data.get('section', content.section)
    content.key = data.get('key', content.key)
    content.value = data.get('value', content.value)
    content.content_type = data.get('content_type', content.content_type)
    
    db.session.commit()
    
    return jsonify(content.to_dict())

@content_bp.route('/content/<int:content_id>', methods=['DELETE'])
@cross_origin()
def delete_content(content_id):
    """حذف المحتوى"""
    content = Content.query.get_or_404(content_id)
    db.session.delete(content)
    db.session.commit()
    
    return jsonify({'message': 'Content deleted successfully'})

@content_bp.route('/client-logos', methods=['GET'])
@cross_origin()
def get_client_logos():
    """جلب شعارات العملاء"""
    logos = ClientLogo.query.order_by(ClientLogo.order_index).all()
    return jsonify([logo.to_dict() for logo in logos])

@content_bp.route('/client-logos', methods=['POST'])
@cross_origin()
def create_client_logo():
    """إضافة شعار عميل جديد"""
    data = request.get_json()
    
    logo = ClientLogo(
        name=data['name'],
        image_path=data['image_path'],
        order_index=data.get('order_index', 0)
    )
    
    db.session.add(logo)
    db.session.commit()
    
    return jsonify(logo.to_dict()), 201

@content_bp.route('/client-logos/<int:logo_id>', methods=['PUT'])
@cross_origin()
def update_client_logo(logo_id):
    """تحديث شعار العميل"""
    logo = ClientLogo.query.get_or_404(logo_id)
    data = request.get_json()
    
    logo.name = data.get('name', logo.name)
    logo.image_path = data.get('image_path', logo.image_path)
    logo.order_index = data.get('order_index', logo.order_index)
    
    db.session.commit()
    
    return jsonify(logo.to_dict())

@content_bp.route('/client-logos/<int:logo_id>', methods=['DELETE'])
@cross_origin()
def delete_client_logo(logo_id):
    """حذف شعار العميل"""
    logo = ClientLogo.query.get_or_404(logo_id)
    db.session.delete(logo)
    db.session.commit()
    
    return jsonify({'message': 'Client logo deleted successfully'})

