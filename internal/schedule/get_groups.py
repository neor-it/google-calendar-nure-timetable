import requests
import urllib.request


class Groups:
    def get_all_groups(self):
        """Returns a dictionary of all groups with their names and IDs."""
        groups = {}
        group_info = self.__get_groups_json()['university']['faculties']

        for faculty in group_info:
            for direction in faculty['directions']:
                groups.update(self.__extract_groups(direction))

        return groups

    @staticmethod
    def __extract_groups(direction):
        groups = {}

        # Try to extract groups from 'groups' key
        group_list = direction.get('groups')
        if group_list is not None:
            for group in group_list:
                groups[group['name']] = group['id']
            return groups

        # If 'groups' key is not present, try to extract from 'specialities' key
        for specialty in direction['specialities']:
            for group in specialty['groups']:
                groups[group['name']] = group['id']

        return groups

    @staticmethod
    def __get_groups_json():
        """Fetches and returns the JSON data from the API."""
        response = requests.get(
            'https://cist.nure.ua/ias/app/tt/P_API_GROUP_JSON',
            proxies=urllib.request.getproxies())
        return response.json()
