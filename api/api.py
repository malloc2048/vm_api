from flask import Flask, request
from flask_restplus import Resource, Api
from utils import token_required, get_vm_info_by_name, get_all_vm_details

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret'

authorizations = {
    'api_token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-auth'
    }
}

# initialize the api functions
api = Api(app, title='Elegant Waterfall', version='v0.1', doc='/')
swagger = api.namespace(
    'elegant_waterfall',
    description='Virtual Machine Interactions',
    authorizations=authorizations,
    security='api_token',
    decorators=[token_required]
)

VM_STATE = {
    1: 'running',
    3: 'paused',
    5: 'shutoff',
}


@swagger.route('/status')
@api.doc(security='api_token')
class Status(Resource):
    @api.response(200, 'API is up and accepting requests')
    @api.response(401, 'Unauthorized')
    def get(self):
        """ Return the current status of the API """
        return 'api is up and running'


@swagger.route('/vm/names')
@api.doc(security='api_token')
class VMNames(Resource):
    @api.response(200, 'list of VM names')
    def get(self):
        """ Return the current state of the requested VM """
        details = get_all_vm_details()

        if not details:
            return f'unable to get VM names', 500

        vm_names = list()
        for detail in details:
            vm_names.append(detail[0].name())
        return {'VM names': vm_names}


@swagger.route('/vm/state')
@api.doc(security='api_token', params={'name': 'A VM Name'})
class VMState(Resource):
    @api.response(200, 'VM state')
    @api.response(400, 'Bad Request please provide VM Name')
    def get(self):
        """ Return the current state of the requested VM """
        args = request.args
        vm_name = args.get('name', None)

        if vm_name:
            domain = get_vm_info_by_name(vm_name)
            if domain:
                vm_state = VM_STATE.get(domain.state()[0], 'UNKNOWN')
            else:
                return f'unable to get VM state for {vm_name}', 400
        else:
            return 'please provide a VM name', 400
        return {'VM State': vm_state}


@swagger.route('/vm/info')
@api.doc(security='api_token', params={'name': 'A VM Name'})
class VMInfo(Resource):
    @api.response(200, 'VM info')
    @api.response(400, 'Bad Request please provide VM Name')
    def get(self):
        """ Return the VM information """
        args = request.args
        vm_name = args.get('name', None)

        if not vm_name:
            return 'missing vm identification', 400

        details = get_all_vm_details()
        for detail in details:
            if detail[0].name() == vm_name:
                return detail[1]
        return {'message': f'unable to get info for {vm_name}'}, 404


@swagger.route('/vm/control')
@api.doc(security='api_token', params={'name': 'A VM Name', 'state': 'new VM state one of {start|stop|restart}'})
class VMState(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request please provide VM Name and desired state')
    def put(self):
        """ Change the VM state """
        args = request.args

        if not args.get('name'):
            return 'missing vm identification', 400
        if not args.get('state'):
            return 'missing desired new state', 400

        vm_info = get_vm_info_by_name(args.get('name'))
        if args.get('state') == 'stop':
            if vm_info.state()[0] != 5:
                vm_info.destroy()
                return {'message': 'vm stopping'}
            else:
                return {'message': 'vm already stopped'}

        elif args.get('state') == 'start':
            if vm_info.state()[0] == 1:
                return {'message': 'vm already running'}
            else:
                vm_info.create()
                return {'message': 'vm starting'}

        elif args.get('state') == 'restart':
            if vm_info.state()[0] == 5:
                vm_info.create()
            else:
                vm_info.reset()

        else:
            return {'error': f'unknown state requested {args.get("state")}'}, 400
