from flask import request, jsonify, abort
# local import
from instance.config import db, app
from api.v1.models import Bucketlist, Items

@app.route('/api/v1/bucketlists/', methods=['GET', 'POST'])
def bucketlists():
    if request.method == 'GET':
        bucketlists = Bucketlist.get_all()
        result = []
        if not bucketlists:
            response = {'message': "No bucketlists have been created"}
            response.update({'status_code': '204'})
            return jsonify(response)
        else:
            for bucketlist in bucketlists:
                items = []
                for item in bucketlist.items:
                    obj = {
                        'id': item.id,
                        'name': item.name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified
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
            response.update({'status_code': '200'})
            return jsonify(response)
    else:
        name = request.data.get('name', '')
        if name:
            bucketlist = Bucketlist(name)
            bucketlist.save()
            response = {'message': "Successfully Created"}
            response.update({'status_code':'201'})
            return jsonify(response)

@app.route('/api/v1/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def bucketlist_manipulation(id, **kwargs):
    # retrieve a buckelist using it's ID
    bucketlist = Bucketlist.query.filter_by(id=id).first()
    if not bucketlist:
        response = {'message': "Invalid bucketlist id"}
        response.update({'status_code': '404'})
        return jsonify(response)

    if request.method == 'DELETE':
        bucketlist.delete()
        response = {'message': "bucketlist {} deleted successfully".format(bucketlist.name)}
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
        response = jsonify({
            'id': bucketlist.id,
            'name': bucketlist.name,
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified
        })
        response.status_code = 200
        return response

@app.route('/api/v1/bucketlists/<int:id>/items/', methods=['POST'])
def add_items(id):
    bucketlist = Bucketlist.query.filter_by(id=id).first()
    items = bucketlist.items
    item_name = request.data.get('name')
    item_check = [item.name for item in items if item.name == item_name]
    if item_check:
        response = jsonify({'Warning': 'this item already exists in the bucketlist'})
        response.status_code = 409
        return response

    if item_name:
        item = Items(item_name, id)
        item.save()
        response = {'message': "Bucketlist item successfully Created"}
        response.update({'status_code':'201'})
        return jsonify(response)

@app.route('/api/v1/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
def edit_item(id,item_id):
    if request.method == 'PUT':
        item = Items.query.filter_by(id=item_id).first()
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
