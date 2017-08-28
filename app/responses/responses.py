from flask import jsonify, make_response

class Response:
	""" Custom API Responses """

	def __init__(self):
		""" Initialize my Responses """
		self.ok_status = 200
		self.created_status = 201
		self.bad_request_status = 400
		self.unauthorized_status = 401
		self.forbidden_status = 403
		self.not_found_status = 404
		self.not_acceptable_status = 406
		self.conflict_status = 409
		self.internal_server_error_status = 500

	@staticmethod
	def define_bucketlist(bucketlist):
		""" Return a dictionary of the bucketlist object """
		obj = {
			'id': bucketlist.id,
			'name': bucketlist.name,
			'date_created': bucketlist.date_created,
			'date_modified': bucketlist.date_modified,
			'created_by': bucketlist.created_by
		}
		return obj
	@staticmethod
	def define_bucketlist_item(bucketlist_item):
		""" Return a dictionary of the bucketlist_item object """
		obj = {
			'id': bucketlist_item.id,
			'name': bucketlist_item.name,
			'date_created': bucketlist_item.date_created,
			'date_modified': bucketlist_item.date_modified,
			'belongs_to': bucketlist_item.belongs_to
		}
		return obj


class Success(Response):
	""" The Successful Requests """

	def complete_request(self, message):
		""" Any Successfull Request """
		response = jsonify({ "message": message })
		return make_response(response), self.ok_status

	def create_resource(self, resource):
		""" Creation of any Resource """
		return make_response(resource), self.created_status


class Error(Response):
	""" The Errneous Requests """

	def not_found(self, message):
		""" Resource not found in User domain """
		response = jsonify({ "error": message })
		return make_response(response), self.not_found_status

	def not_acceptable(self, message):
		""" Request has been understood but not accepted """
		response = jsonify({ "error": message })
		return make_response(response), self.not_acceptable_status

	def causes_conflict(self, message):
		""" Request made causes conflict """
		response = jsonify({ "error": message })
		return make_response(response), self.conflict_status

	def unauthorized(self, message):
		""" Request has an invalid token """
		response = jsonify({ "error": message})
		return make_response(response), self.unauthorized_status

	def forbid_action(self, message):
		""" Request made requires a token, none provided """
		response = jsonify({ "error": message })
		return make_response(response), self.forbidden_status

	def bad_request(self, message):
		""" Request made in the wrong format """
		response = jsonify({ "error": message })
		return make_response(response), self.bad_request_status

	def internal_server_error(self, message):
		""" An error that was not anticipated """
		response = jsonify({ "error": message })
		return make_response(response), self.internal_server_error_status






