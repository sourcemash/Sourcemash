from flask_assets import Environment, Bundle

css_vendor = Bundle("scss/vendor/materialize/materialize.scss", 
                    filters="pyscss", output="css/vendor.css")

js_vendor = Bundle("js/vendor/materialize/*.js",
                    filters="jsmin", output="js/vendor.min.js")

js_default = Bundle("js/default.js",
					filters="jsmin", output="js/default.min.js")

def init_app(app):
    webassets = Environment(app)
    webassets.url = app.static_url_path
    webassets.register('css_vendor', css_vendor)
    webassets.register('js_vendor', js_vendor)
    webassets.register('js_default', js_default)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug