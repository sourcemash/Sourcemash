from flask import redirect, url_for
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from sourcemash.database import db
from sourcemash.models import Feed

admin = Admin()


class FeedView(ModelView):
    can_create = False
    can_delete = False

    def is_accessible(self):
        return current_user.is_authenticated() and \
               current_user.email == "admin@sourcemash.com"

    def _handle_view(self, name, **kwargs):
            if not self.is_accessible():
                return redirect(url_for('security.login'))

    column_display_pk = True
    form_columns = ['title', 'topic', 'public', 'image_url']


admin.add_view(FeedView(Feed, db.session))
