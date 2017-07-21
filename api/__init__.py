from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response
from instance.config import app_config

db = SQLAlchemy()
def create_app(config_name):
    from api.v1.models import Bucketlist, Items, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/v1/bucketlists/', methods=['GET', 'POST'])
    def bucketlists():
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            response = {'message': "Access denied. Please login."}
            response.update({'status_code': '401'})
            return jsonify(response)
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                if request.method == 'GET':
                    limit = 20
                    page = 1
                    search_param = None
                    if request.args.get("limit"):
                        limit = int(request.args.get("limit"))
                    if limit > 100:
                        limit = 100
                    if request.args.get("page"):
                        page = int(request.args.get("page"))
                    if request.args.get("q"):
                        search_param = str(request.args.get("q"))
                    bucketlists = Bucketlist.get_all(user_id, limit, page, search_param)
                    result = []
                    if not bucketlists:
                        response = {'message': "No bucketlists found"}
                        response.update({'status_code': '204'})
                        return jsonify(response)
                    else:
                        for bucketlist in bucketlists.items:
                            items = []
                            for item in bucketlist.items:
                                obj = {
                                    'id': item.id,
                                    'name': item.name,
                                    'date_created': item.date_created,
                                    'date_modified': item.date_modified,
                                    'done': item.done
                                }
                                items.append(obj)
                            bucket = {
                                'id': bucketlist.id,
                                'name': bucketlist.name,
                                'date_created': bucketlist.date_created,
                                'date_modified': bucketlist.date_modified,
                                'items': items
                            }
                            result.append(bucket)
                        response = {'bucketists': result}
                        response.update(
                            {'pagination': {
                                'has_next': bucketlists.has_next,
                                'has_prev': bucketlists.has_prev,
                                'next_num': bucketlists.next_num,
                                'prev_num': bucketlists.prev_num}
                            })
                        response.update({'status_code': '200'})
                        return jsonify(response)
                else:
                    # POST
                    name = request.data.get('name', '')
                    if name:
                        bucketlist = Bucketlist(name, user_id)
                        bucketlist.save()
                        response = {'message': "Successfully Created"}
                        response.update({'status_code':'201'})
                        return jsonify(response)
        else:
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401

    @app.route('/api/v1/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            response = {'message': "Access denied. Please login."}
            response.update({'status_code': '401'})
            return jsonify(response)

        if access_token:
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if bucketlist is None:
                    abort(404)

                if request.method == 'DELETE':
                    bucketlist.delete()
                    response = {
                        'message': "bucketlist {} deleted successfully".format(bucketlist.name)}
                    response.update({'status_code':'200'})
                    return jsonify(response)

                elif request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    bucketlist.name = name
                    bucketlist.save()
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified
                    })
                    response.status_code = 200
                    return response
                else:
                    # GET
                    items = []
                    for item in bucketlist.items:
                        obj = {
                            'id': item.id,
                            'name': item.name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'done': item.done
                        }
                        items.append(obj)
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'items': items
                    })
                    response.status_code = 200
                    return response
        else:
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401

    @app.route('/api/v1/bucketlists/<int:bucket_id>/items/', methods=['POST'])
    def add_items(bucket_id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            response = {'message': "Access denied. Please login."}
            response.update({'status_code': '401'})
            return jsonify(response)
        if access_token:
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=bucket_id).first()
                if bucketlist is None:
                    abort(404)
                items = bucketlist.items
                item_name = request.data.get('name')
                item_check = [item.name for item in items if item.name == item_name]
                if item_check:
                    response = jsonify({'Warning': 'this item already exists in the bucketlist'})
                    response.status_code = 409
                    return response

                if item_name:
                    item = Items(item_name, bucket_id)
                    item.save()
                    response = {'message': "Bucketlist item successfully Created"}
                    response.update({'status_code':'201'})
                    return jsonify(response)
        else:
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401

    @app.route('/api/v1/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
    def item_manipulation(id, item_id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            response = {'message': "Access denied. Please login."}
            response.update({'status_code': '401'})
            return jsonify(response)
        if access_token:
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                item = Items.query.filter_by(id=item_id).first()
                if item is None:
                    abort(404)
                if request.method == 'PUT':
                    item_name = str(request.data.get('name'))
                    if item_name:
                        item.name = item_name
                        item.save()
                        response = jsonify({
                            'id': item.id,
                            'name': item.name,
                            'bucketlist_id':item.bucketlist_id,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified
                        })
                        response.status_code = 200
                        return response
                else:
                    # DELETE
                    item.delete()
                    response = {'message': "Item {} deleted successfully".format(item.name)}
                    response.update({'status_code':'200'})
                    return jsonify(response)

    from .v1.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
