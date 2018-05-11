
import matplotlib.pyplot as plt
import pymysql
import os

class DrawPlot(object):

    def draw(self, data, sql):
        db = pymysql.connect('localhost', 'root', '123456', 'traffic')
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            plt.figure()
            plt.xlabel('hours')
            plt.ylabel('speed')
            plt.title('Street id: ' + id)
            x = []
            y = []
            print('plot')
            for item in result:
                x.append(item[1])
                y.append(item[0])
            print('x')
            print(x)
            print('y')
            print(y)

            plt.plot(x, y)

            if os.path.exists('./traffic/Data/figure.jpg'):
                os.remove('./traffic/Data/figure.jpg')
            print('save page')
            plt.savefig('./traffic/Data/figure.jpg')
            plt.close()

            print(result)
        except Exception as e:
            print(e)
        db.close()