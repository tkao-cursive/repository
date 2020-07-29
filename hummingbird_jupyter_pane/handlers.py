import json


from notebook.base.handlers import APIHandler
from notebook.utils import url_path_join
import tornado
import os
import sys

path_to_hummingbird = os.getenv('HUMMINGBIRD_PATH')
sys.path.append(path_to_hummingbird)

from hummingbird.recorder import Recorder
from hummingbird.player import Player

class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post, 
    # patch, put, delete, options) to ensure only authorized user can request the 
    # Jupyter server
    #@tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /hummingbird-jupyter-pane/get_example endpoint!"
        }))

class RecordHandler(APIHandler):
    @tornado.web.authenticated
    def post(self):
        print('WE ARE RECORDING!')
        # check if state is sent in request, then we know it's not a new recording
        post_data = tornado.escape.json_decode(self.request.body)

        # start recording
        recorder = Recorder(path_to_hummingbird)
        recorder.record()
        recorder.add_cues_to_all_states()

        # return the list of states to the frontend
        self.finish(recorder.data['states'])


class SaveHandler(APIHandler):
    pass

class DeleteHandler(APIHandler):
    pass

class PlaybackHandler(APIHandler):
    pass

class GetHandler(APIHandler):
    pass

def setup_handlers(web_app):
    host_pattern = ".*$"
    
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "hummingbird-jupyter-pane", "get_example")
    record_pattern = url_path_join(base_url, "hummingbird-jupyter-pane", "record")
    save_pattern = url_path_join(base_url, "hummingbird-jupyter-pane", "save/%s")
    delete_pattern = url_path_join(base_url, "hummingbird-jupyter-pane", "delete/%s")
    playback_pattern = url_path_join(base_url, "hummingbird-jupyter-pane", "generatePlayback")
    get_pattern = url_path_join(base_url, "hummingbird-jupyter-pane", "get/%s")
    handlers = [(route_pattern, RouteHandler), 
    (record_pattern, RecordHandler), 
    (save_pattern, SaveHandler), 
    (delete_pattern, DeleteHandler),
    (playback_pattern, PlaybackHandler),
    (get_pattern, GetHandler)]
    web_app.add_handlers(host_pattern, handlers)
