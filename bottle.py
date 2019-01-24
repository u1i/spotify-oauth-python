from bottle import default_app, route, request, response, post, run

@route('/spapp')
def ga():
    out = spapp_do(request.query)
    return out
