from muddle.plugins.plugin import Plugin
from muddle.plugins.models.view import ModelView, ModelListView
from muddle.plugins.models.form import ModelEditView

from models import *


class Devices(Plugin):
    description = 'Provides models and views for tracking.'
    objects = (
        Device,
        NetworkCard,
        ModelView(Device),
        ModelListView(Device),
        ModelEditView(Device)
    )


class Inventory(Plugin):
    description = 'Provides models and views for tracking inventory of a server room.'
    depends = Devices
    objects = (
        Location,
        Rack,
        RackU,
        ModelView(Rack),
        Closet,
        ClosetLocation
    )