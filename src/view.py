import datetime


class View():

    def numerated_array(self, array: list):
        num = 0
        for item in array:
            print(num, '-', item)
            num += 1

    def get_int(self, target):
        print('Enter', target)
        v = input()
        if v:
            return int(v)
        else:
            return None

    def get_float(self, target):
        print('Enter', target)
        v = input()
        if v:
            return float(v)
        else:
            return None

    def get_str(self, target):
        print('Enter', target)
        v = input()
        if v:
            return v
        else:
            return None

    def get_date(self, target):
        print('Enter', target, '(ISO-8601)')
        v = input()
        if v:
            datetime.datetime.strptime(v, '%Y-%m-%d')
            return v
        else:
            return None

    def dict_str(self, dictionary, level=0):
        result = '\t'
        length = len(dictionary)
        i = 1
        for key, value in dictionary.items():
            if type(value) is list:
                result += '\n' + self.list_str(value, key, '')
            else:
                result += str(key) + ' - ' + str(value) + ('' if i == length else ', ')
            i += 1
        return result

    def list_str(self, container, entity, action='Found', level=0):
        tabs = '\t' * level
        action_formatted = '' if len(action) == 0 else action + ' '
        result = ''
        if not container or container is None and action == 'Found':
            result += tabs + 'Not found\n'
        elif container is None:
            result += tabs + entity + 's is None\n'
        elif type(container) is not list:
            result += tabs + action_formatted + entity + ':\n' + self.dict_str(container, level + 1) + '\n'
        elif len(container) == 1:
            result += tabs + action_formatted + entity + ':\n' + self.dict_str(container[0], level + 1) + '\n'
        else:
            result += tabs + action_formatted + entity + 's:\n'
            for item in container:
                result += tabs + self.dict_str(item, level + 1) + '\n'
        print(result)
        return result

    def show_error(self, target, reason=None):
        if reason:
            print("'" + target + "'", "has incorrect", reason)
        else:
            print("'" + target + "'", "cannot be None")

