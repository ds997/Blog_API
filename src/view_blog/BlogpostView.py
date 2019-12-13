from flask import request, g, Blueprint, json, Response
from ..shared_blog.Authentication import Auth
from ..model_blog.BlogpostModel import BlogPostModel, BlogpostSchema

blogpost_api = Blueprint('blogpost_api', __name__)
blogpost_schema = BlogpostSchema()


@blogpost_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
  Create Blogpost Function
  """
    req_data = request.get_json()
    req_data['owner_id'] = g.user.get('id')
    data, error = blogpost_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    post = BlogPostModel(data)
    post.save()
    data = blogpost_schema.dump(post).data
    return custom_response(data, 201)


# add this function
@blogpost_api.route('/', methods=['GET'])
def get_all():
  """
  Get All Blogposts
  """
  posts = BlogPostModel.get_all_blogposts()
  data = blogpost_schema.dump(posts, many=True).data
  return custom_response(data, 200)


def custom_response(res, status_code):
    """
  Custom Response Function
  """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
