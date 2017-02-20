import requests
requests.packages.urllib3.disable_warnings() #disable warnings for not checking local ssl certs


class Ecovent:
    """Class for interacting with the local Ecovent hub"""
    TOKEN_ENDPOINT = "api/v1/token"
    STATUS_ENDPOINT = "api/v1/status"
    ROOM_ENDPOINT = "api/v1/room"
    SCENES_ENDPOINT = "api/v1/scene"
    SET_SCENE_ENDPOINT = "api/v1/active_scene"
    
    REQUEST_TIMEOUT = 5.0
    
    ROOMS = []
    ROOMS_DATA = []
    SCENES = []

    def __init__(self, device_ip, hub_pwd):
        """Initialize the API object"""
        self.host_uri = device_ip + ":60000"
        self.hub_pwd = hub_pwd
        self.token = None
        self._logged_in = False

    def get_token(self):
        """Log into the hub"""
        global TOKEN
        
        params = {
            'hub_pwd': self.hub_pwd
        }
        
        try:
            login = requests.post(
                'https://{host_uri}/{token_endpoint}'.format(
                    host_uri=self.host_uri,
                    token_endpoint=self.TOKEN_ENDPOINT),
                    json=params,
                    timeout=self.REQUEST_TIMEOUT,
                    verify=False
            )
    
        except requests.exceptions.HTTPError as ex:
            print ("Error: ", ex)
            
        try:
            self.token = login.json()['token']
        except KeyError:
            return False
            
        return True
    
    def get_rooms(self):
        """Get defined rooms"""
        if not self._logged_in:
            self._logged_in = self.get_token()
        
        try:
            rooms = requests.get(
                'https://{host_uri}/{status_endpoint}'.format(
                    host_uri=self.host_uri,
                    status_endpoint=self.STATUS_ENDPOINT),
                    headers={
                        'Authorization': "token=" + self.token
                    },
                    verify=False
            )
    
            return rooms.json()['room_status']
        
        except requests.exceptions.HTTPError as ex:
            print ("Error: ", ex)
            return False

    def get_rooms_data(self):
        """Get rooms data"""
        rooms = self.get_rooms()
        
        room_details = []
        
        for attribute in rooms:
            room = {}
            try:
                room_data = requests.put(
                    'https://{host_uri}/{room_endpoint}/{room_id}'.format(
                        host_uri=self.host_uri,
                        room_endpoint=self.ROOM_ENDPOINT,
                        room_id=attribute['id']),
                        headers={
                            'Authorization': "token=" + self.token
                        },
                        verify=False
                )
                room['id'] = attribute['id']
                room['name'] = room_data.json()['name']
                room['humidity'] = round(attribute['humidity'], 1)
                room['pressure'] = round(attribute['pressure'], 1)
                room['temp'] = round (attribute['temp'] * 9/5 + 32, 1)
                room_details.append(room)
                
                
            except requests.exceptions.HTTPError as ex:
                print ("Error: ", ex)
                
        print(room_details)
        return room_details

    def get_all_scenes(self):
        """Get Available Scenes"""
        
        scenes1 = []
        
        try:
            scenes_request = requests.get(
                'https://{host_uri}/{scenes_endpoint}'.format(
                    host_uri=self.host_uri,
                    scenes_endpoint=self.SCENES_ENDPOINT),
                    headers={
                        'Authorization': "token=" + self.token
                    },
                    verify=False
            )
            
            scenes = scenes_request.json()['scenes']
            
        except requests.exceptions.HTTPError as ex:
                print ("Error: ", ex)
                
        for scene in scenes:
            scenes2 = {}
            scenes2['id'] = scene['id']
            scenes2['name'] = scene['name']
            scenes1.append(scenes2)
            
        print("Scenes:", scenes1)
    
    def get_active_scene(self):
        """Get Active Scenes"""
        try:
            scenes_request = requests.get(
                'https://{host_uri}/{scenes_endpoint}'.format(
                    host_uri=self.host_uri,
                    scenes_endpoint=self.SCENES_ENDPOINT),
                    headers={
                        'Authorization': "token=" + self.token
                    },
                    verify=False
            )
            
            active_scene = scenes_request.json()['active_scene']['current_scene_id']
            
        except requests.exceptions.HTTPError as ex:
                print ("Error: ", ex)
            
        print("Active Scene:", active_scene)
    
    def set_active_scene(self, scene_id):
        """Change the active scence"""
        params = {
            'id': scene_id
        }
        
        try:
            rooms_request = requests.put(
                'https://{host_uri}/{set_scene_endpoint}'.format(
                    host_uri=self.host_uri,
                    set_scene_endpoint=self.SET_SCENE_ENDPOINT),
                    json=params,
                    headers={
                        'Authorization': "token=" + self.token
                    },
                    verify=False
            )
    
            print ("New Active Scene:", rooms_request.json()['active_scene']['current_scene_id'])
    
        except requests.exceptions.HTTPError as ex:
            print ("Error: ", ex)
