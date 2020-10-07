from src.Controller.App.Blueprints.thumbnail_blueprint_class import ThumbnailBlueprint
from flask import request, send_file, jsonify
import PIL

"""
    A thumbnail service blueprint
"""

thumb_bp = ThumbnailBlueprint('thumbnail_service', __name__)


@thumb_bp.route('/')
def process_thumbnail():
    img_url = request.args.get('url')
    img = thumb_bp.image_reader.read_image(img_url)
    curr_input = [img, int(request.args.get('width')), int(request.args.get('height'))]
    _id = thumb_bp.hasher.hash_data(curr_input)
    if thumb_bp.data_manager.is_exist(_id):
        img_io = thumb_bp.data_manager.retrieve(_id)
    else:
        img = thumb_bp.converter.convert(img, curr_input[1], curr_input[2])
        if _id != -1:
            thumb_bp.data_manager.put(_id, img)
        img_io = thumb_bp.utils.bytes_to_bytesIO(thumb_bp.utils.image_to_bytes(img))
    return send_file(img_io, mimetype='image/jpeg')


@thumb_bp.errorhandler(PIL.UnidentifiedImageError)
def handle_bad_url(e):
    response = thumb_bp.error_responses.getResponse(400)
    return jsonify(response), 400


@thumb_bp.errorhandler(ValueError)
@thumb_bp.errorhandler(TypeError)
def handle_wrong_parameters(e):
    response = thumb_bp.error_responses.getResponse(422)
    return jsonify(response), 422


@thumb_bp.errorhandler(404)
def handle_requested_url_not_found():
    response = thumb_bp.error_responses.getResponse(404)
    return jsonify(response), 404


@thumb_bp.app_errorhandler(Exception)
def handle_unexpected_error(e):
    response = thumb_bp.error_responses.getResponse(500)
    return jsonify(response), 500
