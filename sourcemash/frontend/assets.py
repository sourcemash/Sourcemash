from flask_assets import Environment, Bundle

css_vendor = Bundle("scss/vendor/materialize/materialize.scss",
                    filters="pyscss", output="css/vendor.css")

css_sourcemash = Bundle("scss/sourcemash.scss",
                    filters="pyscss", output="css/sourcemash.css")

js_vendor = Bundle("js/vendor/jquery.js",
                    "js/vendor/underscore.js",
                    "js/vendor/backbone.js",
                    "js/vendor/backbone.typeahead.js",
                    "js/vendor/materialize.js",
                    filters="jsmin", output="js/vendor.min.js")

js_mixpanel = Bundle("js/vendor/mixpanel.js",
                    filters="jsmin", output="js/mixpanel.min.js")


js_default = Bundle("js/default.js",
					filters="jsmin", output="js/default.min.js")

js_templates = Bundle("../templates/*.tpl",
                        filters="jst",
                        output="js/tpl.js")

js_sourcemash = Bundle("js/sourcemash.js")

js_collections = Bundle("js/collections/*.js")

js_models = Bundle("js/models/*.js")

js_views = Bundle("js/views/help_view.js",
                "js/views/profile_view.js",
                "js/views/footer_view.js",
                "js/views/splash_view.js",
                "js/views/not_found_view.js",
                "js/views/sidenav_view.js",
                "js/views/items_view.js",
                "js/views/loading_view.js",
                "js/views/category_view.js",
                "js/views/feed_view.js",
                "js/views/saved_view.js",
                "js/views/browse_view.js",
                "js/views/feed_topic_view.js",
                "js/views/subscribe_switch_view.js",
                "js/views/subscribe_modal_view.js",
                "js/views/register_modal_view.js",
                "js/views/forgot_modal_view.js",
                "js/views/feed_card_view.js",
                "js/views/item_card_view.js")

js_routers = Bundle("js/routers/*.js")

js_backbone = Bundle(
            js_sourcemash,
            js_models,
            js_collections,
            js_views,
            js_routers,
            filters='jsmin',
            output='js/sourcemash.min.js')


def init_app(app):
    webassets = Environment(app)
    webassets.url = app.static_url_path
    webassets.register('css_vendor', css_vendor)
    webassets.register('css_sourcemash', css_sourcemash)
    webassets.register('js_vendor', js_vendor)
    webassets.register('js_mixpanel', js_mixpanel)
    webassets.register('js_default', js_default)
    webassets.register('js_templates', js_templates)
    webassets.register('js_backbone', js_backbone)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
