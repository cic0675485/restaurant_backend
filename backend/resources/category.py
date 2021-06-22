from flask import request, Response, abort
from schemas.category import CategorySchema
from dto_models.category import Category as CategoryDTO
from services.category import CategoryService
from functools import partial
from dbo_models.category import Category as CategoryDBO
from uuid import UUID
import logging
logger = logging.getLogger(__name__)

class CategoryResource:
    @staticmethod
    def get_by_id(id: UUID) -> Response:
        try:
            returned_dto = CategoryService().get_by_id(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = CategorySchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True) #get from body
            schema = CategorySchema()
            validated_json = schema.load(json) #Validated data from frontend
            dto = CategoryDTO(**validated_json) #transform to DTO OBJECT

            returned_dto = CategoryService().create(dto)
        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource post 400 {}".format(e))
        # except ObjectAlreadyExists as e:
        #     abort(400, {'message': str(e)})
        #     logger.debug("CategoryResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource post 500 {}".format(e))

        #Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")
    
    @staticmethod
    def get_all_categories() -> Response:
        try:
            returned_dto = CategoryService().get_all_categories()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = CategorySchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def update_category(id: UUID) -> Response:
        #
        returned_dto = CategoryService().update_Category(id)
        #
        schema = CategorySchema()
        response_data = schema.dumps(returned_dto)
        #return the response
        return Response(response_data, status=200, headers={}, mimetype="application/json")
        pass
    
    @staticmethod
    def delete_category(id: UUID) -> Response:
        #call the delete method of the category resource, get back the deleted category object
        returned_dto = CategoryService().delete_Category(id)
        #serialize the category object into json
        schema = CategorySchema()
        response_data = schema.dumps(returned_dto)
        #return the response
        return Response(response_data, status=200, headers={}, mimetype="application/json")
        pass