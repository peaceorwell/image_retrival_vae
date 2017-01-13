from myapp import app, mysql
import numpy as np

class database:
    def __init__(self):
        pass

    def search_top(self, coarse_str, fine_str, num, scale):
        conn = mysql.connect()
        cursor = conn.cursor()
        if scale == '400':
            table_name = 'lung_l'
        elif scale == '100':
            table_name = 'lung_m'
        else:
            table_name = 'lung_m'
        table_name = 'level_1'
        cursor.execute("select * from %s where coarse_key = %s"%(table_name, coarse_str))
        new_complete_list = list(cursor.fetchall())
        if len(new_complete_list) < num:
            cursor.execute('select id,coarse_key from %s'%table_name)
            fetch_infos = cursor.fetchall()
            new_list = []
            for len_hanming in xrange(1, 47):
                if len(new_list) > num - 1:
                    break
                for info in fetch_infos:
                    if self.hanming(info[1], coarse_str) == len_hanming:
                        new_list.append(info)
            for info in new_list:
                cursor.execute("select * from %s where id = %d"%(table_name, info[0]))
                fetch_info = cursor.fetchall()
                new_complete_list.append(fetch_info[0])

            res_dict = dict()
            idx = 0
            for one_res in new_complete_list:
                len_res = self.similarity(one_res[2], fine_str)
                res_dict[idx] = len_res
                idx += 1
            sort_res = sorted(res_dict.items(), key=lambda d: d[1])

            if len(new_complete_list) > 0:
                show_cnt = min(num, len(new_complete_list))
            else:
                show_cnt = 0
            files = []
            for i in xrange(show_cnt):
                file_info = []
                print sort_res[i][1]
                file_info.append(new_complete_list[sort_res[i][0]][3])
                file_info.append(new_complete_list[sort_res[i][0]][4])
                files.append(file_info)
            cursor.close()
            conn.close()
            return files
        else:
            res_dict = dict()
            idx = 0
            for one_res in new_complete_list:
                len_res = self.similarity(one_res[2], fine_str)
                res_dict[idx] = len_res
                idx += 1
            sort_res = sorted(res_dict.items(), key=lambda d: d[1])

            if len(new_complete_list) > 0:
                show_cnt = min(num, len(new_complete_list))
            else:
                show_cnt = 0
            files = []
            for i in xrange(show_cnt):
                file_info = []
                print sort_res[i][1]
                file_info.append(new_complete_list[sort_res[i][0]][3])
                file_info.append(new_complete_list[sort_res[i][0]][4])
                files.append(file_info)
            cursor.close()
            conn.close()
            return files
    def str2array(self, str_input):
        return np.array([int(y, 2) for y in list(str_input)])

    def fine2array(self, str_input):
        return np.array([float(y) for y in str_input.split(';')])

    def hanming(self, input1, input2):
        array1 = self.str2array(input1)
        array2 = self.str2array(input2)
        res_xor = array1 ^ array2
        return len(np.nonzero(res_xor)[0])

    def similarity(self, input1, input2):
        array1 = self.fine2array(input1)
        array2 = self.fine2array(input2)
        array3 = (array1 - array2)**2
        return array3.sum()

    '''
    def get_types_tumor(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from types_tumor")
        res_list = cursor.fetchall()
        cursor.close()
        conn.close()
        res_dict = dict()
        for info in res_list:
            res_dict[int(info[0])] = info[1]
        return res_dict
        '''
