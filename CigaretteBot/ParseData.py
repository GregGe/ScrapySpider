import json

class ParseData():

    def read_name(self):
        name_list = []
        with open('name.txt') as file:
            for name in file:
                name = file.readline()
                names = name.split('（')[0].split('(')
                name_list.append(names[0])

        return set(sorted(name_list))

    def write_name(self,list):
        with open("brand.txt",'w') as file:
            for name in list:
                if '\n' in name:
                    file.write(name)
                else:
                    file.write(name+'\n')

    def amend_name(self):
        with open("name_amend.txt",'w') as amend_file:
            with open("name.txt") as file:
                for name in file:
                    name = file.readline()
                    name = name.replace('(','').replace(')','')
                    name = name.replace('（','').replace('）','')
                    amend_file.write(name)



if __name__ == '__main__':

    #para_data = ParseData()
    #para_data.write_name(para_data.read_name())
    #para_data.amend_name()
    with open("cigarette.json",'r') as file:
        json = json.load(file)
        for item in json:
            print(item['name'])
            print(item['price'])
            print(item['img'])
    pass